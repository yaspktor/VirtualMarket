
import yfinance as yf # real time stock price
from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
   
    return render_template("apology.html", top=code, bottom=message), code


def login_required(f):
    """
    Decorate routes to require login.

    
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    try:
        ticker = yf.Ticker(symbol).info
        print(ticker["currentPrice"])
        
    except:
        print("Error ticker")
        return None
  
    try:
        #quote = response.json()
        market_price = ticker['currentPrice']
        #print(market_price)
        #pre_market_price = ticker['preMarketPrice']
        return {
            "name": ticker["longName"],
            "price": float(market_price),
            "symbol": symbol
        }
    except (KeyError, TypeError, ValueError):
        print("Error dict")
        #print error type
        print(KeyError)
        
        return None
def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def companyDesc(symbol):
    try: 
        desc = yf.Ticker(symbol).info
        news = yf.Ticker(symbol).news
        return {
            "desc": desc["longBusinessSummary"],
            "news": news
        }
    except:
        print("Error CompanyDesc")
        return None
    
    
    

    