from flask import Flask, flash, redirect, render_template, request, session
import datetime
import sqlite3
from helpers import apology
from flask import Blueprint, render_template, abort
from werkzeug.security import check_password_hash, generate_password_hash
#import from main app con 
from helpers import usd



register_blueprint = Blueprint('register', __name__, template_folder='templ')

@register_blueprint.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        if request.form.get('login'):
            return redirect("/login")
        if not request.form.get("username"):
            return apology("must provide username", 400)

        else:
            con = sqlite3.connect("finance.db", check_same_thread=False)
            db = con.cursor()
            rows = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchall()
            if rows:
                print(rows[0][1])
                error = 'Username already exists'
                con.close()
                return apology(error, 400)
            else:
                if not request.form.get("password") or not request.form.get("confirmation"):
                    error = 'must provide password'
                    con.close()
                    return apology(error, 400)
                elif request.form.get("password") != request.form.get("confirmation"):
                    error = 'passwords are not the same'
                    con.close()
                    return apology(error, 400)
                # all is corerect
                else:
                    hash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
                    if hash:
                        data_to_insert =  (request.form.get("username"), hash)
                        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", data_to_insert)
                        con.commit()
                        id = db.execute("SELECT id FROM users WHERE username = ?", (request.form.get("username"),)).fetchall()[0][0]
                        session["user_id"] = id
                        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", (session["user_id"],)).fetchall()[0][0]
                        session["user_cash"] = usd(user_cash)
                        con.close()
                        return redirect("/")
                    else:
                        error = 'cannot generate hash'
                        con.close()
                        return apology(error, 400)

    else:
        return render_template("register.html")