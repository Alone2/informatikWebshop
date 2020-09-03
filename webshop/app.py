from flask import Flask, url_for, abort, render_template, session, request, redirect, Response
import drinksdatabase
import time
import sys
import drinkshtml
import user
import random

app = Flask(__name__)
app.secret_key = "87zihkjnl"
db = None
CATEGORIES = None

@app.route("/", methods=["GET"])
def home():
    logged_in = user.is_logged_in(session)
    c = db.get_category(1) # category 1 => beliebt -> startseite
    drinks = db.get_drinks_by_category(c)
    return drinkshtml.generate_homepage(logged_in, CATEGORIES, drinks)

@app.route("/login", methods=["POST","GET"])
def login():
    failed = ""
    logged_in = user.is_logged_in(session)
    if request.method == "POST":
        uname = request.form["username"]
        pswrt = request.form["password"]
        success = user.login(uname, pswrt, session, db)
        if success:
            return redirect("/")
        failed = "Wrong password"
    return drinkshtml.generate_loginpage(logged_in, False, CATEGORIES ,failedMessage=failed)

@app.route("/register", methods=["POST","GET"])
def register(): 
    failed = ""
    logged_in = user.is_logged_in(session)
    if request.method == "POST":
        uname = request.form["username"]
        pswrt = request.form["password"]
        pswrt2 = request.form["password2"]
        if pswrt != pswrt2:
            failed = "The 2 passwords did not match."
        elif pswrt == "":
            failed = "Password insecure"
        else: 
            db.begin()
            try:
                db.create_user(uname, pswrt)
            except:
                db.revert()
                return drinkshtml.generate_loginpage(logged_in, True, failedMessage="Error! Name exist or internal error") 
            db.commit()
            success = user.login(uname, pswrt, session, db)
            if success:
                return redirect("/")
            failed = "You registered. Cannot log in: nternal error"
    return drinkshtml.generate_loginpage(logged_in, True, CATEGORIES, failedMessage=failed)

@app.route("/logout", methods=["POST","GET"])
def logout():
    user.logout(session)
    return redirect("/")
        
@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    userid = user.get_userid(db, session)
    item = request.form["item"]
    drink = db.get_drink(item)
    db.begin()
    try:
        db.add_to_cart(userid, drink)
        db.commit()
    except Exception as e:
        print("Error" , e, flush=True)
        db.revert()
    return redirect("/cart")

@app.route("/remove_from_cart", methods=["POST"])
def remove_from_cart():
    userid = user.get_userid(db, session)
    item = request.form["item"]
    drink = db.get_drink(item)
    db.begin()
    try:
        db.remove_from_cart(userid, drink)
        db.commit()
    except:
        db.revert()
    return redirect("/cart")

@app.route("/buy_cart", methods=["POST"])
def buy_cart():
    userid = user.get_userid(db, session)
    db.begin()
    try:
        db.buy_cart(userid)
        db.commit()
    except Exception as e:
        print(e, flush=True)
        print("lel", flush=True)
        db.revert()
    return redirect("/")

@app.route("/cart", methods=["GET"])
def cart():
    logged_in = user.is_logged_in(session)
    drinks = []
    if logged_in:
        order_warenkorb = db.get_cart(user.get_userid(db, session))
        return drinkshtml.generate_warenkorb(logged_in, order_warenkorb, CATEGORIES)
    return redirect("/")

@app.route("/search", methods=["GET"])
def search():
    logged_in = user.is_logged_in(session)
    searchterm = request.args.get("term")
    category = request.args.get("category")
    drinks = []
    # print(category)
    if category != "" and category != None:
        cat = db.get_category(int(category))
        drinks = db.get_drinks_by_category(cat)
    elif searchterm != "" and searchterm != None:
        drinks = db.get_drinks_search(searchterm)
    else:
        return abort(404)
    return drinkshtml.generate_searchpage(logged_in, drinks, CATEGORIES, False, searchterm=searchterm, category=category)

@app.route("/img", methods=["GET"])
def img():
    drinkid = request.args.get("item")
    d = db.get_drink(drinkid)
    imgs = db.get_images(d)
    if len(imgs) <= 0:
        return Response("", mimetype="image/png")
    return Response(random.choice(), mimetype="image/png")

@app.route("/test")
def test():
    return drinkshtml.navigation(CATEGORIES)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # If using Docker
        if sys.argv[1] == "True":
            # tries to access database 12 times
            # and checks if its online / accessible
            db = drinksdatabase.Database(app, isDocker=True)
            for i in range(6):
                # needs to be in app context to access database
                print("Waiting for connection with database...", flush=True)
                try:
                    with app.app_context():
                        if db.can_connect():
                            break
                except:
                    pass
                time.sleep(3)
    if db == None:
        db = drinksdatabase.Database(app, isDocker=False, user="root", password="ef21")
    with app.app_context():
        CATEGORIES = db.get_all_categories()
    app.run(host="0.0.0.0", port=8080, debug=True)
