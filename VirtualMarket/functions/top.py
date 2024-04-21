from flask import Flask, flash, redirect, render_template, request, session
import datetime
import sqlite3
from helpers import apology, login_required, lookup, usd, companyDesc
from flask import Blueprint, render_template, abort
#import from main app con 




top_blueprint = Blueprint('top', __name__, template_folder='templ')


@top_blueprint.route("/top", methods=["GET", "POST"])
@login_required
def top():
    con = sqlite3.connect("finance.db", check_same_thread=False)
    db = con.cursor()
    users = db.execute("SELECT username, cash, id FROM users ORDER BY cash DESC ").fetchall()
    totals = [] # tablica słoowników z nazwą użytkownika i jego portfelem
    # słownik aby trzymac tam symbol i aktualną cene akcji, po to zeby nie pytac api ciagle o to samo
    prices = {}
    #dla kazdego uzytkownika w bazie:
    for user in users:
        #print(user['username'])
        rows = db.execute(
            "SELECT symbol, user_id, SUM(shares) as Shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", (user[2],)).fetchall()

        total = user[1]
        # dla kazgej akcji w portfelu uzytkownika
        for row in rows:
            #print symbol
            #print(f'Symbol: {row["symbol"]}')
            symbol = row[0]
            # pobranie z bazy ceny akcji z tabeli stocks
            price = db.execute("SELECT price FROM stocks WHERE symbol = ?", (symbol,)).fetchall()[0][0]
            
            total += int(row[2]) * float(price)

        totals.append([user[0], total])
        #print(total)
    totals.sort(reverse=True, key=lambda x: x[1])
    con.close()
    return render_template("top.html", users=totals, usd=usd)

