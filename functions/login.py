from flask import Flask, flash, redirect, render_template, request, session
import datetime
import sqlite3
from helpers import apology
from flask import Blueprint, render_template, abort
from werkzeug.security import check_password_hash, generate_password_hash
#import from main app con 
from helpers import usd



login_blueprint = Blueprint('login', __name__, template_folder='templ')


@login_blueprint.route("/login", methods=["GET", "POST"])
def login():

    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if request.form.get('register'):
            return redirect("/register")
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        con = sqlite3.connect("finance.db", check_same_thread=False)
        db = con.cursor()
        rows = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            return apology("invalid username and/or password", 403)


        
        # Remember which user has logged in
        session["user_id"] = rows[0][0]
        session["username"] = request.form.get("username")
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", (session["user_id"],)).fetchall()[0][0]
        session["user_cash"] = usd(user_cash)
        # Redirect user to home page
        con.close()
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")