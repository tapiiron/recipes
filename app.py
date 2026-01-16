import sqlite3
import re

from flask import Flask
from flask import render_template,flash,redirect,request,session

import markupsafe

import db
import usercontrol

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/user/create",methods=["POST"])
def user_create():
    username = request.form["username"]
    password = request.form["password"]
    password2 = request.form["password2"]
    if password != password2:
        flash("Error: Passwords do not match!")
        return redirect("/user/create")
    try:
        usercontrol.create_user(username,password)
    except sqlite3.IntegrityError:
        flash("Error: Username already in use")
        return redirect("/user/create")
    return redirect("/")

@app.route("/user/login",methods=["GET","POST"])
def user_login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form("username")
        password = request.form("password")

        user_id = usercontrol.check_login(username,password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            flash("Error: Invalid username or password")
            return redirect("/login")

