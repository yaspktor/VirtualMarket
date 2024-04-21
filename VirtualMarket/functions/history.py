from flask import Flask, flash, redirect, render_template, request, session
import datetime
import sqlite3
from helpers import apology, login_required, lookup, usd, companyDesc
from flask import Blueprint, render_template, abort
#import from main app con 
from update import update_new_element


history_blueprint = Blueprint('history', __name__, template_folder='templ')

@history_blueprint.route("/history")
@login_required
def history():
    con = sqlite3.connect("finance.db", check_same_thread=False)
    db = con.cursor()
    """Show history of transactions"""
    rows = db.execute("SELECT symbol, shares, price, date FROM transactions WHERE user_id = ? ORDER BY date DESC",
                      (session["user_id"],)).fetchall()
    
    
    con.close()
    return render_template("history.html", rows=rows, usd=usd)

