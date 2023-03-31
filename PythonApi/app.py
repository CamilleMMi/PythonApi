from flask import Flask
from flask import url_for
from flask import request
from flask import render_template
from flask import session
from flask import redirect
from pathlib import Path
from markupsafe import escape
import logging
import sqlite3
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# flash pour les messages


def get_db():
    return sqlite3.connect("instance/db.sqlite")


if not Path("instance/db.sqlite").exists():
    db = get_db()
    sql = Path("db.sql").read_text()
    db.executescript(sql)


def checkSession():
    if "username" not in session:
        return None
    return session["username"]


@app.route("/login", methods=["POST", "GET"])
def login():
    error = None
    if request.method == "POST":
        if valid_login(request.form["username"], request.form["password"]):
            conn = get_db()
            result = conn.execute(
                "SELECT id, email FROM users WHERE username = ?",
                [request.form["username"]],
            )
            row = result.fetchone()
            session["id"] = row[0]
            session["email"] = row[1]
            session["username"] = request.form["username"]
            conn.close()
            return redirect(url_for("index"))
        else:
            error = "Invalid username/password"
    return render_template("login.html", error=error)


def valid_login(username, password):
    conn = get_db()
    result = conn.execute("SELECT password FROM users WHERE username = ?", [username])
    row = result.fetchone()
    conn.close()
    if row is not None and row[0] == password:
        return True
    else:
        return False


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


@app.route("/register", methods=["POST", "GET"])
def register():
    error = None
    if request.method == "POST":
        if register_user(
            request.form["username"], request.form["password"], request.form["email"]
        ):
            return redirect(url_for("index"))
        else:
            error = "Registration failed"
    return render_template("register.html", error=error)


def register_user(username, password, email):
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            [username, password, email],
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        conn.rollback()
        conn.close()
        return False


@app.route("/")
def index():
    username = checkSession()
    if username is None:
        return redirect(url_for("login"))
    return render_template("index.html", username=username)


@app.route("/addWatchList")
def addWatchList():
    return render_template("addWatchList.html")
