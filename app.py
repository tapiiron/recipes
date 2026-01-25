import sqlite3
import re

from flask import Flask
from flask import render_template,flash,redirect,request,session

import markupsafe

import db
import usercontrol
import recipecontrol
import config

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    recipes = recipecontrol.list_recipies()
    return render_template("index.html",recipes=recipes)

@app.route("/user/register")
def register():
    return render_template("register.html")

@app.route("/user/create",methods=["POST"])
def user_create():
    username = request.form["username"]
    password = request.form["password"]
    password2 = request.form["password2"]
    if password != password2:
        flash("Error: Passwords do not match!")
        return redirect("/user/register")
    try:
        usercontrol.create_user(username,password)
    except sqlite3.IntegrityError:
        flash("Error: Username already in use")
        return redirect("/user/register")
    return redirect("/")

@app.route("/user/login",methods=["GET","POST"])
def user_login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form["username"].lower()
        password = request.form["password"]

        user_id = usercontrol.check_login(username,password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            flash("Error: Invalid username or password")
            return redirect("/user/login")

@app.route("/user/logout")
def user_logout():
    session.clear()
    return redirect("/")

@app.route("/recipe/add",methods=["GET","POST"])
def recipe_add():
    if request.method == "GET":
        return render_template("recipe_add.html")
    else:
        return redirect("/")