from flask import Flask, flash, redirect, render_template, request, session
import datetime
import sqlite3
from helpers import apology, login_required, lookup, usd, companyDesc
from flask import Blueprint, render_template
#import from main app con 
from update import update_new_element


quote_blueprint = Blueprint('quote', __name__, template_folder='templ')

@quote_blueprint.route("/quote", methods=["GET", "POST"])
@login_required
def quote():    
    con = sqlite3.connect("finance.db", check_same_thread=False)
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        if not symbol:
            error = "missing quote"
            return apology(error, 400)
        else:
            con = sqlite3.connect("finance.db", check_same_thread=False)
            db = con.cursor() 
            user_shares = db.execute("SELECT SUM(shares) as shares FROM transactions WHERE user_id = ? AND symbol = ?",
                                 (session["user_id"], symbol)).fetchall()[0][0]
            
            if user_shares == None:
                user_shares = 0
            
            quote = lookup(symbol)
            data = companyDesc(symbol)
            if quote and data:
                #update price in database 
                update_new_element(quote)
                #quote = lookup(symbol)
                # print(quote)
                con.close()
                return render_template("quote.html", quote=quote, usd=usd, data=data, min=min,user_shares=user_shares)
            else:
                error = "invalid symbol"
                con.close()
                return apology(error, 400)
    else:
        db = con.cursor() 
        symbols = db.execute("SELECT symbol, name FROM stocks").fetchall()
        # company_names = db.execute("SELECT name FROM stocks").fetchall()
        
        
        con.close()
        return render_template("quote.html", symbols=symbols)

