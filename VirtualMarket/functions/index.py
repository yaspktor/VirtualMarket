from flask import Flask, flash, redirect, render_template, request, session
import datetime
import sqlite3
from helpers import apology, login_required, lookup, usd, companyDesc
from flask import Blueprint, render_template, abort
from werkzeug.security import check_password_hash, generate_password_hash
#import from main app con 


con = sqlite3.connect("finance.db", check_same_thread=False)

index_blueprint = Blueprint('index', __name__, template_folder='templ')


@index_blueprint.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    db = con.cursor()
    rows = db.execute(
        "SELECT symbol, SUM(shares) as Shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", (session["user_id"],)).fetchall()
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", (session["user_id"],)).fetchall()[0][0]
    print("user cash", user_cash)
    names = {}
    prices = {}
    #dic of profits for each stock symbol {"stock_name" : "profit"}
    profits={}
    
    total = user_cash
    print(f"user: {total}")
    for row in rows:
        symbol = row[0]
        
        # instead of lookup, use db to get price from stocks table       
        lk = db.execute("SELECT price, name FROM stocks WHERE symbol = ?", (symbol,)).fetchall()[0]
        #print("lk:" ,lk)
        if lk:
            prices[symbol] = lk[0]
            names[symbol] = lk[1]
            print(int(row[1]) * float(lk[0]))
            total += int(row[1]) * float(lk[0])
            actual_price = prices[symbol] * row[1]
            historical_price = 0
            #caltulate profit, get data from transactions table and compare with actual price
            history = db.execute("SELECT price, shares FROM transactions WHERE user_id = ? AND symbol = ?", (session["user_id"], symbol)).fetchall()
            
            for row in history:
                historical_price += row[0] * row[1]
            profits[symbol] = actual_price - historical_price
                
            
        else:
            return apology("Błąd, odśwież stronę", 400)
    print(total)
    #session['user_cash'] = usd(user_cash)
    return render_template("index.html", rows=rows, names=names, prices=prices, usd=usd, cash=user_cash, total=total , profits=profits)