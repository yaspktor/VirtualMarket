import sqlite3
import yfinance as yf
import datetime

def lookup(symbol):

    try:
        ticker = yf.Ticker(symbol).info
        print(ticker["currentPrice"])
        
    except:
        print("Error ticker")
        return None
    # Parse response
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







con = sqlite3.connect("finance.db")

db = con.cursor()


def update_new_element(data):
    #check if symbol exist in stocks
    currentDateTime = datetime.datetime.now()
    con2 = sqlite3.connect('finance.db')
    db = con2.cursor()
    rows = db.execute("SELECT  symbol FROM stocks").fetchall()
    symbols = []
    for row in rows:
        symbols.append(row[0])
    
        
    if data["symbol"] not in symbols:
        print("not exist")
        print(data["symbol"])
        print(symbols)
        data_to_insert = (data["name"], data["symbol"], data["price"], currentDateTime)
        db.execute("INSERT INTO stocks (name, symbol, price, last_update) VALUES (?, ?, ?, ?)",data_to_insert)
        con2.commit()
        print("added new element")
    else:
        print("exist")
    con2.close()
    
user_shares = db.execute("SELECT SUM(shares) as shares FROM transactions WHERE user_id = ? AND symbol = ?",
                                 ("17", "MCD")).fetchall()[0][0]

print(user_shares)
symbols = db.execute("SELECT symbol FROM stocks").fetchall()
print(symbols[2][0])   
symbols = db.execute("SELECT symbol, name FROM stocks").fetchall()
for el in symbols:
    print(el)

#update_new_element(lookup("DIS"))