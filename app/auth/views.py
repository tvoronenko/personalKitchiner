from flask import Blueprint
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from app.auth.models import *
from app import app
from app.helpers import apology, login_required
from werkzeug.security import check_password_hash, generate_password_hash

mod = Blueprint('auth', __name__)


# log in
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form['username']
        password = request.form['password']
        error = None
        # Query database for username
        rows = get_user(username)

        # Ensure username exists and password is correct
        if len(rows) != 1:
            error = 'Incorrect username.'
        elif not check_password_hash(rows[0]["hash"], password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]
            # Redirect user to home page
            return redirect("/")
        return apology(error, 400)
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("auth/login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# registeration of user
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        error = None
        try:
            # Query database for username
            hash = generate_password_hash(password)
            new_user_id = create_new_user(username, hash)
        except ValueError:
            error = f"User {username} is already registered."
        else:
            session["user_id"] = new_user_id
            # Redirect user to home page
            return redirect("/")
        if error is not None:
            return apology(error, 400)
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("auth/register.html")
