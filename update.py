
from helpers import lookup
import sqlite3
import time
import datetime


def update_table_prices():
    # połączenie z bazą danych
    currentDateTime = datetime.datetime.now()
    con = sqlite3.connect('finance.db')
    db = con.cursor()
    #print all symbols from stocks
    rows = db.execute("SELECT  symbol, price, last_update FROM stocks").fetchall()
    for row in rows:
        #jesli last update jest starszy niz 3 minuty to update
        
        last_update_datetime = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S.%f')
        if last_update_datetime < currentDateTime - datetime.timedelta(minutes=3):
            #print(row[0])
            data = lookup(row[0])
            #print(data)
            data_to_insert = (data["price"], currentDateTime, row[0])
            db.execute("UPDATE stocks SET price = ?, last_update = ? WHERE symbol = ?", data_to_insert)
            con.commit()
            print(f"updated symbol {row[0]}")
            #print(data_to_insert)
            #print("update")
    con.close()

#funkcja ktora wywoluje update co  3 minuty

def update_loop():
    while True:
        update_table_prices()
        time.sleep(180)
   
   
#funkcja ktora dodaje nowe elementy jesli nie istnieja w stocks data = lookup(symbol)
#jesli uzytkownik wpisze gdziekolwiek nowy symbol czy to w quote, sell, buy to dodaje go do stocks, aby zbyt czesto nie wywolywac funkcji lookup z helpers.py

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
        print(f"added new element{data['symbol']}")
    elif data["symbol"] in symbols:
        #update price and last update
        data_to_update = (data["price"], currentDateTime, data["symbol"])
        db.execute("UPDATE stocks SET price = ?, last_update = ? WHERE symbol = ?", data_to_update)
        con2.commit()
        print(f"updated price for: {data['symbol']}")
        
    else:
        print("exist")
    con2.close()
   
