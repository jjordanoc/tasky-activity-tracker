from flask import render_template, redirect, Flask, session, request, url_for, flash, jsonify, make_response
from functions import login_required
from psycopgtools import create_connection, execute_query, execute_fetch_query
from werkzeug.security import generate_password_hash, check_password_hash
from os import environ
import datetime


""" Setup app and database """
app = Flask("__name__")
app.secret_key = "a76&ohljasdt7&jYUHas/(jasdu"

environ["printQuerys"] = "True"
environ["printQueryResult"] = "True"

DATABASE_URL = environ['DATABASE_URL']
database = create_connection(DATABASE_URL)

create_table_users = """CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);"""

create_table_buttons = """CREATE TABLE IF NOT EXISTS buttons (
    user_id INTEGER,
    name TEXT NOT NULL,
    timespan TEXT NOT NULL,
    multiplier TEXT NOT NULL,
    color TEXT NOT NULL,
    reset_date TEXT NOT NULL,
    count INTEGER DEFAULT 0,
    button_id SERIAL PRIMARY KEY,
    FOREIGN KEY (user_id) REFERENCES users(id)
);"""

execute_query(database, create_table_users)
execute_query(database, create_table_buttons)


@app.route("/")
@login_required
def index():
    """ Show user's buttons and update current state if needed"""
    # Template name
    template = "index.html"

    # Get all the buttons that correspond to this user
    buttons = execute_fetch_query(database, "SELECT * FROM buttons WHERE user_id=%s;", session["user_id"])

    # Get current date in YYYY-MM-DD format
    curr_date = datetime.date.today()

    # Iterate over all buttons to reset expired ones
    for button in buttons:
        rd_str = button['reset_date']
        print(rd_str)
        # If reset date is not set to manual
        if rd_str != "Manual":
            button_id = button['button_id']
            # Transform given date from string to date type
            reset_date = datetime.datetime.strptime(rd_str, "%Y-%m-%d").date()
            delta = reset_date-curr_date
            print(delta)
            # If delta days is negative or equal to 0, it means the current date is greater than or equal to the reset date, thus, we reset the button
            if delta.days <= 0:

                # Reset count
                print("Resetting count...")
                execute_query(database, "UPDATE buttons SET count=0 WHERE button_id=%s;", button_id)

                #Once count is reset, calculate new reset date
                multiplier = int(button['multiplier'])
                timespan = button['timespan']

                # Get delta needed according to multiplier
                newDelta = None
                if timespan == "days":
                    newDelta = datetime.timedelta(days=multiplier)
                elif timespan == "weeks":
                    newDelta = datetime.timedelta(weeks=multiplier)
                elif timespan == "months":
                    newDelta = datetime.timedelta(weeks=multiplier*4.35)
                elif timespan == "years":
                    newDelta = datetime.timedelta(weeks=multiplier*4.35*12)

                newReset_date = "Manual"
                if newDelta:
                    newReset_date = curr_date + newDelta
                    newReset_date = str(newReset_date)

                # Update new reset date into the database
                execute_query(database, "UPDATE buttons SET reset_date=%s WHERE button_id=%s;", newReset_date, button['button_id'])

            else:
                print("Not resetting button")
        else:
            print("Passing")

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
        user_dict_list = execute_fetch_query(database, "SELECT * FROM users WHERE username=%s;", username)
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
        if execute_fetch_query(database, "SELECT username FROM users WHERE username=%s;", username):
            flash("Username already exists")
            return render_template(template)

        # Hash password
        password = generate_password_hash(password)

        # Insert user data into the database
        execute_query(database, "INSERT INTO users (username, password) VALUES (%s, %s);", username, password)

        # Check if session is valid
        tmpid = execute_fetch_query(database, "SELECT id FROM users WHERE username=%s;", username)

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
    # Get username
    username = execute_fetch_query(database, "SELECT username FROM users WHERE id=%s;", session['user_id'])
    # Error check
    if not username:
        flash("Log in error, please log-in again")
        return redirect("/login")
    # Get the username
    username = username[0]['username']
    return render_template(template, username=username)


@app.route("/reset", methods=["POST"])
@login_required
def reset():
    """ Reset the button with the given id """
    # Get the button's id
    button_id = request.form.get("button_id")

    # Update the button's count
    execute_query(database, "UPDATE buttons SET count=0 WHERE button_id=%s;", button_id)

    # Send data to AJAX call
    return jsonify({"count" : 0})


@app.route("/remove", methods=["POST"])
@login_required
def remove():
    """ Reset the button with the given id """
    # Get the button's id
    button_id = request.form.get("button_id")

    # Update the button's count
    execute_query(database, "DELETE FROM buttons WHERE button_id=%s;", button_id)

    # Send junk to AJAX call
    return jsonify({"result" : "success"})


@app.route("/reset_buttons", methods=["POST"])
@login_required
def reset_buttons():
    """ Reset the count of all user's buttons """
    # Set count to 0 in the database
    execute_query(database, "UPDATE buttons SET count=0 WHERE user_id=%s;", session["user_id"])
    flash("Successfully reset all buttons")
    return redirect("/")


@app.route("/delete_buttons", methods=["POST"])
@login_required
def delete_buttons():
    """ Delete all of the user's buttons """
    # Delete all buttons in the database
    execute_query(database, "DELETE FROM buttons WHERE user_id=%s;", session["user_id"])
    flash("Successfully deleted all buttons")
    return redirect("/")


@app.route("/change_password", methods=["POST", "GET"])
@login_required
def change_password():
    """ Let the user change his password """
    template = "change.html"

    if request.method == "POST":
        # Get data from the form
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Error checking
        if not password or not confirmation:
            flash("Provide valid credentials")
            return render_template(template)
        if password != confirmation:
            flash("Confirmation must match new password")
            return render_template(template)

        # Hash password
        password = generate_password_hash(password)

        # Insert user data into the database
        execute_query(database, "UPDATE users SET password=%s WHERE id=%s;", password, session["user_id"])

        flash("Successfully changed password")
        # Redirect user to index
        return redirect("/")

    else:
        return render_template(template)


@app.route("/delete_account", methods=["POST"])
@login_required
def delete_account ():
    """ Delete user's account from the database """
    # Delete account from the database
    execute_query(database, "DELETE FROM users WHERE id=%s;", session["user_id"])
    # Delete buttons from the database too
    execute_query(database, "DELETE FROM buttons WHERE user_id=%s;", session["user_id"])
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

    # Get current date
    curr_date = datetime.date.today()
    # Get delta needed according to multiplier
    delta = None
    if timespan == "days":
        delta = datetime.timedelta(days=multiplier)
    elif timespan == "weeks":
        delta = datetime.timedelta(weeks=multiplier)
    elif timespan == "months":
        delta = datetime.timedelta(weeks=multiplier*4.35)
    elif timespan == "years":
        delta = datetime.timedelta(weeks=multiplier*4.35*12)

    reset_date = "Manual"
    if delta:
        reset_date = curr_date + delta
        reset_date = str(reset_date)

    # Insert data into buttons database
    execute_query(database, "INSERT INTO buttons (user_id, name, timespan, multiplier, color, reset_date) VALUES (%s, %s, %s, %s, %s, %s);",
                  session["user_id"], name, timespan, multiplier, color, reset_date)

    # Render main page with all the user's buttons
    return redirect("/")


@app.route("/update_count", methods=["POST"])
@login_required
def update_count():
    """ Update the count every press using AJAX """
    # Get id from form submit
    button_id = request.form.get("button_id")

    # Get the current count from the database
    count_dict_list = execute_fetch_query(database, "SELECT count FROM buttons WHERE button_id=%s;", button_id)

    curr_count = int(count_dict_list[0]['count'])

    # Increment the count
    curr_count += 1

    # Update the count
    execute_query(database, "UPDATE buttons SET count=%s WHERE button_id=%s;", curr_count, button_id)

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

