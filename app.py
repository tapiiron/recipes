import sqlite3

from flask import Flask
from flask import render_template,flash,redirect,request,session,abort,make_response
import secrets

import usercontrol
import recipecontrol
import config

app = Flask(__name__)
app.secret_key = config.secret_key

def checksession():
    if session.get("user_id") is None:
        abort(403)

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/",methods=["GET","POST"])
def index():
    if session.get("csrf_token") is None:
        session["csrf_token"] = secrets.token_hex(16)
    tags = recipecontrol.list_tags()
    if request.method == "GET":
        recipes = recipecontrol.list_recipes()
        return render_template("index.html",recipes=recipes,tags=tags)
    else:
        check_csrf()
        search = request.form["search"].lower()
        tag = request.form["tag"]
        recipes = recipecontrol.search_recipes(search,tag)
        return render_template("index.html",recipes=recipes,tags=tags,search=search,searchtag=tag)

@app.route("/user/register")
def register():
    if session.get("csrf_token") is None:
        session["csrf_token"] = secrets.token_hex(16)
    return render_template("register.html")

@app.route("/user/create",methods=["POST"])
def user_create():
    check_csrf()
    username = request.form["username"].lower()
    password = request.form["password"]
    password2 = request.form["password2"]
    if password != password2:
        flash("Error: Passwords do not match!")
        return redirect("/user/register")
    if len(username) < 3 or len(username) > 30:
        flash("Error: Username must be between 3 and 30 characters long")
        return redirect("/user/register")
    try:
        usercontrol.create_user(username,password)
    except sqlite3.IntegrityError:
        flash("Error: Username already in use")
        return redirect("/user/register")
    flash("Registered your username "+username+ ". You can now login.")
    return redirect("/user/login")

@app.route("/user/login",methods=["GET","POST"])
def user_login():
    if session.get("csrf_token") is None:
        session["csrf_token"] = secrets.token_hex(16)
    if request.method == "GET":
        return render_template("login.html")
    else:
        check_csrf()
        username = request.form["username"].lower()
        password = request.form["password"]
        if len(username) < 3 or len(username) > 30:
            flash("Error: Username must be between 3 and 30 characters long")
            return redirect("/user/login")
        user_id = usercontrol.check_login(username,password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("Error: Invalid username or password")
            return redirect("/user/login")

@app.route("/user/logout")
def user_logout():
    session['user_id'] = None
    session['username'] = None
    session["csrf_token"] = secrets.token_hex(16)
    return redirect("/")

@app.route("/recipe/add",methods=["GET","POST"])
def recipe_add():
    checksession()
    if request.method == "GET":
        tags = recipecontrol.list_tags()
        return render_template("recipe_add.html",tags=tags)
    else:
        check_csrf()
        user_id = session["user_id"]
        name = request.form["name"]
        ingredients = request.form["ingredients"]
        instructions = request.form["instructions"]
        tags = []
        if request.form.getlist("tags"):
            tags = request.form.getlist("tags")
        if len(name) > 50 or len(ingredients) > 3000 or len(instructions) > 3000:
            flash("Name (max 50 letters), ingredients or instructions field is too long (max 3000 letters), please shorten it.")
            return redirect("/recipe/add")

        recipecontrol.add_recipe(user_id,name,ingredients,instructions,tags)
        flash("Recipe added")
        return redirect("/")
    
@app.route("/recipe/edit/<int:id>",methods=["GET","POST"])
def recipe_edit(id):
    checksession()
    recipe = recipecontrol.load_recipe(id)
    if recipe[0]['id_user']!=session['user_id']:
        abort(403)
    tags = recipecontrol.list_tags()
    tagged_raw=recipecontrol.list_recipe_tag_ids(id)
    tagged=[]
    if tagged_raw != None:
        for tag in tagged_raw:
            tagged.append(tag['id'])
    
    if request.method == "GET":
        return render_template("recipe_edit.html",recipe=recipe[0],tags=tags,tagged=tagged)
    else:
        check_csrf()
        tags = []
        if request.form.getlist("tags"):
            tags = request.form.getlist("tags")
        if len(request.form['name']) > 50 or len(request.form['ingredients']) > 3000 or len(request.form['instructions']) > 3000:
            flash("Name (max 50 letters), ingredients or instructions field is too long (max 3000 letters), please shorten it.")
            return redirect("/recipe/edit/"+str(id))
        recipecontrol.update_recipe(id,request.form['name'],request.form['ingredients'],request.form['instructions'],tags)
        flash("You have successfully edited the recipe")
        return redirect("/recipe/edit/"+str(id))
    
@app.route("/recipe/display/<int:id>")
def display_recipe(id):
    recipe = recipecontrol.load_recipe(id)
    recipetags = recipecontrol.load_recipe_tags(id)
    comments = recipecontrol.get_comments(id)
    if recipe:
        return render_template("recipe_display.html",recipe=recipe[0],recipetags=recipetags,comments=comments)
    else:
        return redirect("/")

@app.route("/comment/add/<int:id>",methods=["POST"])
def add_comment(id):
    checksession()
    check_csrf()
    comment = request.form['comment']
    grade = int(request.form['grade'])
    if len(comment) > 3000:
        flash("Comment is too long (max 3000 letters), please shorten it.")
        return redirect("/recipe/display/"+str(id))
    if grade > 0 and grade < 11:
        recipecontrol.add_comment(id,session['user_id'],comment,grade)
    else:
        flash("Wrong input for comment grade")
    return redirect("/recipe/display/"+str(id))

def delete_comment(id):
    checksession()
    comment=recipecontrol.get_comment(id)
    if comment[0]['id_user'] != session['user_id']:
        abort(401)
    recipecontrol.delete_comment(id)
    flash("Comment deleted")
    return redirect("/recipe/display/"+str(comment[0]['id_recipe']))

def remove_recipe(id):
    checksession()
    recipe = recipecontrol.load_recipe(id)
    if recipe[0]['id_user']!=session['user_id']:
        abort(403)
    recipecontrol.remove_recipe(id)
    flash("Removed recipe "+recipe[0]['name'])
    return redirect("/")

@app.route("/recipe/image/get/<int:id>")
def show_recipe_image(id):
    image = recipecontrol.get_image(id)
    if not image:
        abort(404)
    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/recipe/image/upload/<int:id>",methods=['POST'])
def upload_image(id):
    checksession()
    check_csrf()
    file = request.files['image']
    if not file.filename.endswith(".jpg"):
        flash("ERROR: wrong picture format")
        return redirect("/recipe/edit/"+str(id))
    
    image = file.read()

    if len(image) > 100 * 1024:
        flash("ERROR: Too large image")
        return redirect("/recipe/edit/"+str(id))
    
    recipecontrol.update_picture(id,image)
    flash("You have successfully added image to recipe")
    return redirect("/recipe/edit/"+str(id))

@app.route("/user/show")
def user_show():
    checksession()
    recipes = recipecontrol.list_recipes_by_user(session['user_id'])
    statistics = recipecontrol.show_user_recipe_statistics(session['user_id'])
    return render_template("user_page.html",recipes=recipes,statistics=statistics)

@app.route("/delete/<item>/<int:id>/<int:phase>",methods=['GET','POST'])
def delete_item(item,id,phase):
    checksession()
    if item == None or id < 1 or phase < 1:
        abort(403)
    if request.method == 'GET':
        phase = phase + 1
        return render_template("are_you_sure.html",item=item,id=id,phase=phase)
    check_csrf()
    if phase > 2:
        if item == 'comment':
            return delete_comment(id)
        elif item == 'recipe':
            return remove_recipe(id)
        else:
            abort(403)
    else:
        phase = phase + 1
        return render_template("are_you_sure.html",item=item,id=id,phase=phase)
