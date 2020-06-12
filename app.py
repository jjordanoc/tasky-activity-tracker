from flask import render_template, redirect, Flask, session, request, url_for, flash
from functions import login_required, msg
from sqlitetools import create_connection, execute_query, execute_fetch_query
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta, datetime


""" Setup app and database """
app = Flask("__name__")
app.secret_key = "a76&ohljasdt7&jYUHas/(jasdu"

database = create_connection("database.db")

@app.route("/")
@login_required
def index():
    # Template name
    template = "index.html"

    # Get all the buttons that correspond to this user
    buttons = execute_fetch_query(database, "SELECT * FROM buttons WHERE user_id=?", session["user_id"])

    # Render main page with all the user's buttons
    return render_template(template, buttons=buttons)


@app.route("/login", methods=["GET", "POST"])
def login():
    """ Logs the user in """
    # Clear any session
    session.clear()
    # Template name
    template = "login.html"

    if request.method == "POST":
        # Get data from the form
        username = request.form.get("username")
        password = request.form.get("password")

        # Error checking
        if not username or not password:
            return msg(template, "Invalid credentials", "warning")

        # Get data from this user
        dbRow = execute_fetch_query(database, "SELECT * FROM users WHERE username=?;", username)
        # Check if passwords match and username exists
        if len(dbRow) != 1 or not check_password_hash(dbRow[0][2], password):
            return msg(template, "Invalid credentials", "danger")
        
        # Save user id
        session["user_id"] = dbRow[0][0]

        # Redirect user to index
        return redirect("/")
    else:
        return render_template(template)

@app.route("/register", methods=["GET", "POST"])
def register():
    """ Register the user """
    # Clear any session
    session.clear()
    # Template name
    template = "register.html"

    if request.method == "POST":
        # Get data from the form
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Error checking
        if not username or not password or not confirmation:
            return msg(template, "Provide valid credentials", "warning")
        if password != confirmation:
            return msg(template, "Confirmation must match password", "warning")
        if execute_fetch_query(database, "SELECT username FROM users WHERE username=?;", username):
            return msg(template, "Username already exists", "danger")

        # Hash password
        password = generate_password_hash(password)

        # Insert user data into the database
        execute_query(database, "INSERT INTO users (username, password) VALUES (?, ?);", username, password)

        # Check if session is valid
        tmpid = execute_fetch_query(database, "SELECT id FROM users WHERE username=?;", username)

        # Store session
        session["user_id"] = tmpid[0][0]

        # Redirect user to index
        return redirect("/")

    else:
        return render_template(template)

@app.route("/logout")
def logout():
    """ Log out the user """
    # Forget any user id's
    session.clear()
    
    # Redirect user to login
    return redirect("/login")


@app.route("/update", methods=["POST"])
@login_required
def update():
    """ Update the page """

    if request.method == "POST":
        
        # Get data from the form
        button_name = request.form.get("name")
        timespan = request.form.get("timespan")
        multiplier = request.form.get("multiplier")
        button_color = request.form.get("color")

        # Error check
        if not button_name or not timespan or not multiplier:
            flash("Invalid arguments", "danger")
            return redirect("/")

        # Insert data into buttons database
        execute_query(database, "INSERT INTO buttons (user_id, button_name, timespan, multiplier, color) VALUES (?, ?, ?, ?, ?);", 
                      session["user_id"], button_name, timespan, multiplier, button_color)

        # Render main page with all the user's buttons
        return redirect("/")

    



if __name__ == "__main__":
    app.run(debug=True)

