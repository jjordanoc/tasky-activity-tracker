from flask import render_template, redirect, Flask, session, request, url_for, flash, jsonify, make_response
from functions import login_required
from sqlitetools import create_connection, execute_query, execute_fetch_query
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta, datetime
from os import environ


""" Setup app and database """
app = Flask("__name__")
app.secret_key = "a76&ohljasdt7&jYUHas/(jasdu"

database = create_connection("database.db")

environ["printQuerys"] = "True"
environ["printQueryResult"] = "True."


@app.route("/")
@login_required
def index():
    """ Show all of the user's buttons """
    # Template name
    template = "index.html"

    # Get all the buttons that correspond to this user
    buttons = execute_fetch_query(database, "SELECT * FROM buttons WHERE user_id=?;", session["user_id"])

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
            flash("Invalid credentials")
            return render_template(template)

        # Get data from this user
        user_dict_list = execute_fetch_query(database, "SELECT * FROM users WHERE username=?;", username)
        # Check if passwords match and username exists
        if len(user_dict_list) != 1 or not check_password_hash(user_dict_list[0]["password"], password):
            flash("Invalid credentials")
            return render_template(template)
        
        # Save user id
        session["user_id"] = user_dict_list[0]["id"]

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
            flash("Provide valid credentials")
            return render_template(template)
        if password != confirmation:
            flash("Confirmation must match password")
            return render_template(template)
        if execute_fetch_query(database, "SELECT username FROM users WHERE username=?;", username):
            flash("Username already exists")
            return render_template(template)

        # Hash password
        password = generate_password_hash(password)

        # Insert user data into the database
        execute_query(database, "INSERT INTO users (username, password) VALUES (?, ?);", username, password)

        # Check if session is valid
        tmpid = execute_fetch_query(database, "SELECT id FROM users WHERE username=?;", username)

        # Store session
        session["user_id"] = tmpid[0]["id"]

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


@app.route("/account")
@login_required
def account():
    """ Show a menu with account options """
    template = "account.html"
    return render_template(template)


@app.route("/reset", methods=["POST"])
@login_required
def reset():
    """ Reset the button with the given id """
    # Get the button's id
    button_id = request.form.get("button_id")

    # Update the button's count
    execute_query(database, "UPDATE buttons SET count=0 WHERE button_id=?;", button_id)

    # Send data to AJAX call
    return jsonify({"count" : 0})


@app.route("/remove", methods=["POST"])
@login_required
def remove():
    """ Reset the button with the given id """
    # Get the button's id
    button_id = request.form.get("button_id")

    # Update the button's count
    execute_query(database, "DELETE FROM buttons WHERE button_id=?;", button_id)

    # Send junk to AJAX call
    return jsonify({"result" : "success"})


@app.route("/reset_buttons", methods=["POST"])
@login_required
def reset_buttons():
    """ Reset the count of all user's buttons """
    # Set count to 0 in the database
    execute_query(database, "UPDATE buttons SET count=0 WHERE user_id=?;", session["user_id"])
    flash("Successfully reset the count of all buttons")
    return redirect("/")


@app.route("/delete_buttons", methods=["POST"])
@login_required
def delete_buttons():
    """ Delete all of the user's buttons """
    # Delete all buttons in the database
    execute_query(database, "DELETE FROM buttons WHERE user_id=?;", session["user_id"])
    flash("Successfully deleted all buttons")
    return redirect("/")


@app.route("/change_password", methods=["POST"])
@login_required
def change_password():
    return redirect("/")


@app.route("/delete_account", methods=["POST"])
@login_required
def delete_account ():
    """ Delete user's account from the database """
    # Delete account from the database
    execute_query(database, "DELETE FROM users WHERE id=?;", session["user_id"])
    # Delete buttons from the database too
    execute_query(database, "DELETE FROM buttons WHERE user_id=?;", session["user_id"])
    flash("Successfully deleted all account data")
    return redirect("/login")


@app.route("/update", methods=["POST"])
@login_required
def update():
    """ Update the page's buttons """
    # Get data from the form
    name = request.form.get("name")
    timespan = request.form.get("timespan")
    multiplier = request.form.get("multiplier")
    color = request.form.get("color")

    # Check for none
    if not multiplier:
        multiplier = 0
    else:
        multiplier = int(multiplier)

    # Error check
    if not name or not timespan:
        flash("Invalid arguments")
        return redirect("/")

    # Insert data into buttons database
    execute_query(database, "INSERT INTO buttons (user_id, name, timespan, multiplier, color) VALUES (?, ?, ?, ?, ?);", 
                  session["user_id"], name, timespan, multiplier, color)

    # Render main page with all the user's buttons
    return redirect("/")


@app.route("/update_count", methods=["POST"])
@login_required
def update_count():
    """ Update the count every press using AJAX """
    # Get id from form submit
    button_id = request.form.get("button_id")

    # Get the current count from the database
    count_dict_list = execute_fetch_query(database, "SELECT count FROM buttons WHERE button_id=?;", button_id)

    curr_count = int(count_dict_list[0]['count'])

    # Increment the count
    curr_count += 1

    # Update the count
    execute_query(database, "UPDATE buttons SET count=? WHERE button_id=?;", curr_count, button_id)

    # Return a JSON object to the AJAX call
    return jsonify({"count" : curr_count})


@app.errorhandler(400)
def bad_request():
    """ Page not found """
    flash("400 error, bad request")
    return make_response(redirect("/"), 400)


@app.errorhandler(404)
def not_found():
    """ Page not found """
    flash("404 error, could not find page")
    return make_response(redirect("/"), 404)

@app.errorhandler(500)
def server_error():
    """ Page not found """
    flash("500 error, internal server error")
    return make_response(redirect("/"), 500)

# Execute application
if __name__ == "__main__":
    app.run()

