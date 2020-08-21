from flask import Flask, render_template, session, request, redirect
import drinksdatabase
import time
import sys
import drinkshtml
import user

# wait till database is up
time.sleep(10)


app = Flask(__name__)
app.secret_key = "87zihkjnl"
db = None

@app.route("/")
def home():
    return drinkshtml.generate_homepage(user.is_logged_in(session))

@app.route("/login", methods=["POST,GET"])
def login():
    failed = ""
    if request.method == "POST":
        uname = request.form["username"]
        pswrt = request.form["password"]
        success = user.login(uname, pswrt)
        if success:
            return redirect("/")
        failed = "Wrong password"
    return drinkshtml.generate_loginpage(user.is_logged_in(session), False, failedMessage=failed)

@app.route("/register", methods=["POST,GET"])
def register(): 
    failed = ""
    if request.method == "POST":
        uname = request.form["username"]
        pswrt = request.form["password"]
        db.begin()
        try:
            db.create_user(uname, pswrt)
        except:
            db.revert()
            return drinkshtml.generate_loginpage(user.is_logged_in(session), True, failedMessage="Error! Name exist or internal error") 
        db.commit()
        success = user.login(uname, pswrt)
        if success:
            return redirect("/")
        failed = "You registered. Cannot log in: nternal error"
    return drinkshtml.generate_loginpage(user.is_logged_in(session), True, failedMessage=failed)

@app.route("/cart")
def cart():
    categories = db.get_all_categories()
    return drinkshtml.generate_warenkorb(user.is_logged_in(session))

@app.route("/search")
def search():
    categories = db.get_all_categories()
    return drinkshtml.generate_searchpage(user.is_logged_in(session), searchterm, drinks, categories)

@app.route("/test")
def test():
    db.begin()
    out = str(db.is_password_correct("test2","test"))
    db.commit()
    return out

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # If using Docker
        if sys.argv[1] == "True":
            db = drinksdatabase.Database(app, True)
    if db == None:
        db = drinksdatabase.Database(app)
    app.run(host="0.0.0.0", port=8080)
