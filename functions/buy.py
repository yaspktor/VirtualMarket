from flask import Flask, flash, redirect, render_template, request, session
import datetime
import sqlite3
from helpers import apology, login_required, lookup, usd, companyDesc
from flask import Blueprint, render_template, abort
#import from main app con 
from update import update_new_element
from helpers import usd



buy_blueprint = Blueprint('buy', __name__, template_folder='templ')


@buy_blueprint.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    
    if request.method == "POST":
        
        if not request.form.get("symbol"):
            return apology("missing symbol", 400)
        elif not request.form.get("shares").isnumeric():
            return apology("invalid shares", 400)
        elif not request.form.get("shares") or int(request.form.get("shares")) <= 0:
            return apology("missing shares", 400)

        lk = lookup(request.form.get("symbol"))
        if not lk:
            return apology("invalid symbol", 400)
        else:
            # check if can buy
            con = sqlite3.connect("finance.db", check_same_thread=False)
            db = con.cursor()
            shares = int(request.form.get("shares"))
            user_cash = float(db.execute("SELECT cash FROM users WHERE id = ?", (session["user_id"],)).fetchall()[0][0])
            total = float(lk['price']) * shares
            if total > user_cash:
                return apology("can't afford", 400)
            else:
                currentDateTime = datetime.datetime.now()
                # insert new data to transaction table
                data = (session["user_id"], request.form.get("symbol"), shares, float(lk['price']), currentDateTime)
                db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
                            data)
                con.commit()
                print(" try update")
                update_new_element(lk)
                
                # update user cash
                updated_cash = user_cash - total
                data_update = (updated_cash, session["user_id"])
                db.execute("UPDATE users SET cash = ? WHERE id = ?", data_update)
                con.commit()
                flash("Bought")
                user_cash = db.execute("SELECT cash FROM users WHERE id = ?", (session["user_id"],)).fetchall()[0][0]
                session["user_cash"] = usd(user_cash)
                con.close()
                return redirect("/")

    else:
        
        return render_template("buy.html")