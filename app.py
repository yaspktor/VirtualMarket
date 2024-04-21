from flask import Flask, redirect,  request, session
from flask_session import Session

from flask_limiter.util import get_remote_address
from threading import Thread
from helpers import apology, usd
from functions.buy import buy_blueprint
from functions.login import login_blueprint
from functions.register import register_blueprint
from functions.top import top_blueprint
from functions.index import index_blueprint
from functions.sell import sell_blueprint
from functions.history import history_blueprint
from update import update_loop
from functions.quote import quote_blueprint



# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

#debug mode
app.config["DEBUG"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure database




#new thread to update prices in database

t1 = Thread(target=update_loop)
t1.daemon = True
t1.start()


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.register_blueprint(buy_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(register_blueprint)
app.register_blueprint(top_blueprint)
app.register_blueprint(index_blueprint)
app.register_blueprint(sell_blueprint)
app.register_blueprint(history_blueprint)
app.register_blueprint(quote_blueprint)




@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.errorhandler(429)
def ratelimit_handler(e):
  return apology("You are sending requests too quickly!", 429)


if __name__ == "__main__":
    app.run(debug=True)