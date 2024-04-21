from flask import Flask, flash, redirect, render_template, request, session
import datetime
import sqlite3
from helpers import apology, login_required, lookup, usd, companyDesc
from flask import Blueprint, render_template, abort
#import from main app con 
from helpers import usd



sell_blueprint = Blueprint('sell', __name__, template_folder='templ')


@sell_blueprint.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    """Sell shares of stock"""
    con = sqlite3.connect("finance.db", check_same_thread=False)
    db = con.cursor() 
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("missing symbol", 400)
        elif not request.form.get("shares") or int(request.form.get("shares")) <= 0:
            return apology("missing shares", 400)

        # check if user have enough shares to sell
               
        symbol = request.form.get("symbol")
        user_shares = db.execute("SELECT SUM(shares) as shares FROM transactions WHERE user_id = ? AND symbol = ?",
                                 (session["user_id"], symbol)).fetchall()[0][0]
        if user_shares == None:
            con.close()
            return apology("No shares to sell.", 400)
        
        
        if int(request.form.get("shares")) > user_shares:
            con.close()
            return apology("too many shares", 400)
        else:
            lk = lookup(request.form.get("symbol"))
            price = float(lk["price"])
            total = price * int(request.form.get("shares"))
            db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", (total, session["user_id"]))
            currentDateTime = datetime.datetime.now()
            # insert new data to transaction table
            #data for transaction table
            data_to_insert = (session["user_id"], symbol, -int(request.form.get("shares")), price, currentDateTime)
            db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
                       data_to_insert
                       )
            con.commit()
            flash("sold")
            user_cash = db.execute("SELECT cash FROM users WHERE id = ?", (session["user_id"],)).fetchall()[0][0]
            session["user_cash"] = usd(user_cash)
            con.close()
            return redirect("/")
    else:
        #rows = db.execute("SELECT DISTINCT symbol FROM transactions WHERE user_id = ?", (session["user_id"],))
        rows = db.execute(
        "SELECT symbol, SUM(shares) as Shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", (session["user_id"],)).fetchall()
        #data = rows.fetchall()
        print(rows)
        con.close()
        return render_template("sell.html", rows=rows)


