import os
import sqlite3

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helper import apology, login_required, validate

# Configure application
app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD=True
)

db = sqlite3.connect("bucketList.db", check_same_thread=False)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        dob = request.form.get("dob")

        if password == "" or confirmation == "" or username == "" or dob == "":
            return apology("Empty input", 400)

        if not (password == confirmation):
            return apology("Passwords do not match", 400)

        if not validate(dob):
            return apology("Invalid DOB Format", 400)

        userIndb = db.execute(f"SELECT username FROM users WHERE username='{username}'")

        if userIndb.fetchall():
            return apology("User existed", 400)
        else:
            hashPassword = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
            params = (username, dob, hashPassword)
            db.execute("INSERT INTO users (username, dob, password) VALUES (?, ?, ?)", params)
            db.commit()
            
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            return apology("must provide username", 403)

        elif not password:
            return apology("must provide password", 403)

        name = db.execute(f"SELECT username FROM users WHERE username='{username}'").fetchone()
        pswHash = db.execute(f"SELECT password FROM users WHERE username='{username}'").fetchone()
        id = db.execute(f"SELECT id FROM users WHERE username='{username}'").fetchone()
        
        if not name:
            return apology("Username not exist", 400)
        if not check_password_hash(pswHash[0], password):
            return apology("invalid password", 403)

        session["user_id"] = id[0]

        return render_template("create.html")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    """Buy shares of stock"""
    if request.method == "POST":
        title = request.form.get("title")
        date = request.form.get("date")
        location = request.form.get("location")
        description = request.form.get("location")
        status = "New"
        user_id = session["user_id"]

        if title == "" or date == "" or location == "" or description == "":
            return apology("Empty input", 400)

        params = (user_id, title, date, location, description, status)
        db.execute("INSERT INTO lists (user_id, title, date, location, description, status) VALUES(?, ?, ?, ?, ?, ?)", params)
        db.commit()

        lists = db.execute(f"SELECT * FROM lists WHERE user_id = '{user_id}'")
        results = lists.fetchall()

        return render_template("mylists.html", results = results)

    else:
        return render_template("create.html")


@app.route("/mylists", methods=["GET", "POST"])
@login_required
def lists():
    user_id = session["user_id"]

    if request.method == "GET":
        lists = db.execute(f"SELECT * FROM lists WHERE user_id = '{user_id}'")
        results = lists.fetchall()

        return render_template("mylists.html", results = results)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    if request.method=='POST':
        bucketId = id
        title = request.form.get("title")
        date = request.form.get("date")
        location = request.form.get("location")
        description = request.form.get("description")
        changeStatus = request.form.get('changeStatus')
        print (changeStatus)

        if title == "" or date == "" or location == "" or description == "":
            return apology("Empty input", 400)

        params = ( title, date, location, description, changeStatus )
        db.execute(f"UPDATE lists SET (title, date, location, description, status) =(?, ?, ?, ?, ?) WHERE id = '{bucketId}' ", params)
        db.commit()

        return redirect("/mylists")
    
    else:
        return redirect("/")


@app.route("/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete(id):
    if request.method=='POST':
        bucketId = id

        db.execute("DELETE FROM lists WHERE id = ?", [bucketId])
        flash('List Deleted')
        db.commit()

        return redirect("/mylists")
    
    else:
        return redirect("/")


@app.route('/profile', methods=['GET','POST]'])
@login_required
def profile():
    user_id = session["user_id"]

    if request.method=='GET':
        user = db.execute(f"SELECT * FROM users WHERE id = '{user_id}'")
        result = user.fetchall()

        count = db.execute(f"SELECT COUNT(*) FROM lists WHERE user_id = '{user_id}'").fetchone()
        completedCount = db.execute(f"SELECT COUNT(*) FROM lists WHERE user_id = '{user_id}' AND status = 'Completed'").fetchone()
        pendingCount = db.execute(f"SELECT COUNT(*) FROM lists WHERE user_id = '{user_id}' AND status = 'Pending'").fetchone()

        return render_template("profile.html", result=result, count=count, completedCount=completedCount, pendingCount=pendingCount)
    
    else:
        return render_template("/")


@app.route("/profileDelete/<int:id>", methods=["GET", "POST"])
@login_required
def profileDelete(id):
    if request.method=='POST':
        userId = id

        db.execute("DELETE FROM users WHERE id = ?", [userId])
        db.execute("DELETE FROM lists WHERE user_id = ?", [userId])
        flash('User Deleted')
        db.commit()

        session.clear()
        return redirect("/")
    
    else:
        return redirect("/")