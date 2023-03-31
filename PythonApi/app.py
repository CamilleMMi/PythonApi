from flask import Flask
from flask import url_for
from flask import request
from flask import render_template
from flask import session
from flask import redirect
from pathlib import Path
from markupsafe import escape
import sqlite3
import secrets

# all the differents import used for the project

# global variable, for the name
app = Flask(__name__)

# global variable for a secret key used for the authentication
app.secret_key = secrets.token_hex(16)


# part where we get the db
def get_db():
    return sqlite3.connect("instance/db.sqlite")


# if she doest exist create it on the instance folder
if not Path("instance/db.sqlite").exists():
    db = get_db()
    sql = Path("db.sql").read_text()
    db.executescript(sql)


# a custom function i made to look if the user is logged in, other way of doing were possible but would had required much more time
def checkSession():
    if "username" not in session:
        return None
    return session["username"]


# route where i redirect the user everytime he try to access a ressource without being logged in
@app.route("/login", methods=["POST", "GET"])
def login():
    error = None
    # if the user send a "post" request it means he tried to logg in
    if request.method == "POST":
        # the valid_login make sure the user does exist with the correct informations
        if valid_login(request.form["username"], request.form["password"]):
            conn = get_db()
            # return the user to set variable into the session
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
            # if there is an error error, with that we could have tried to set up an error message on the template
            error = "Invalid username/password"
    return render_template("login.html", error=error)


# the function used to verify the loggin
def valid_login(username, password):
    conn = get_db()
    result = conn.execute("SELECT password FROM users WHERE username = ?", [username])
    row = result.fetchone()
    conn.close()

    if row is not None and row[0] == password:
        return True
    else:
        return False


# used to delete everything about the user of the session and redirect the user to the index wich will redirect the user on the loggin route
@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("email", None)
    session.pop("id", None)

    return redirect(url_for("index"))


# used to register a new user
@app.route("/register", methods=["POST", "GET"])
def register():
    error = None
    if request.method == "POST":
        # calle the register_user function that will create the user on the data base
        if register_user(
            request.form["username"], request.form["password"], request.form["email"]
        ):
            return redirect(url_for("index"))
        else:
            # same for the loggin could be used to display an error message
            error = "Registration failed"

    return render_template("register.html", error=error)


# the sql part of the register
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
    # if there is an error make a rollback to delete every wrong informations and close the data base
    except Exception as e:
        conn.rollback()
        conn.close()

        return False


# main route where the user will be able to disconect, create a new watching_list see his existing watching_list and delete some
@app.route("/")
def index():
    username = checkSession()

    if username is None:
        return redirect(url_for("login"))

    user_id = session.get("id")
    # get every watching_list object the user has , some upgr
    db = get_db()
    watching_list = db.execute(
        "SELECT id, viewing_name, platform, advancement FROM watching_list WHERE user_id = ?",
        [user_id],
    ).fetchall()

    # create an object made by the different attribute needed for the index
    watching_list_formatted = []
    for row in watching_list:
        watching_list_formatted.append(
            {
                "viewing_name": row[1],
                "platform": row[2],
                "advancement": row[3],
                "id": row[0],
            }
        )

    db.commit()
    db.close()

    # Render the template with the data
    return render_template(
        "index.html", username=username, watching_list=watching_list_formatted
    )


@app.route("/addWatchList", methods=["GET", "POST"])
def addItemToWatchList():
    username = checkSession()

    if username is None:
        return redirect(url_for("login"))

    if request.method == "POST":
        # Get the data from the form
        viewing_name = request.form["viewing_name"]
        platform = request.form["platform"]
        advancement = request.form["advancement"]

        # Get the user ID from the session
        user_id = session.get("id")

        # Insert the data into the database
        db = get_db()
        db.execute(
            "INSERT INTO watching_list (viewing_name, platform, advancement, user_id) VALUES (?, ?, ?, ?)",
            (viewing_name, platform, advancement, user_id),
        )
        db.commit()
        db.close()

        # Redirect to the index page
        return redirect(url_for("index"))
    else:
        # Redirect to the add watch list page
        return render_template("addWatchList.html")


@app.route("/deleteItem/<int:item_id>", methods=["POST"])
def deleteItemFromWatchList(item_id):
    username = checkSession()

    if username is None:
        return redirect(url_for("login"))

    # open the db, look wich element the user try to delete and delete it from the data base,
    # if i could do an upgrade i would put the active propertie to false and never delete any data
    db = get_db()
    user_id = session.get("id")
    db.execute(
        "DELETE FROM watching_list WHERE id = ? AND user_id = ?", (item_id, user_id)
    )
    db.commit()
    db.close()

    return redirect(url_for("index"))
