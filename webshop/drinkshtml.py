# https://flask.palletsprojects.com/en/rtd/templating/
from flask import render_template

#
#  LEVEL 0
#

# page /
def generate_homepage(loggedin, categories, drinks, failedMessage = None):
    header = generate_header(loggedin)
    sbar = generate_navigation(categories)
    content = generate_welcome_content(drinks, loggedin)
    return generate_hauptlayout(header, sbar, content)

# page /login and /register
def generate_loginpage(loggedin, doesregister, categories, failedMessage = None):
    header = generate_header(loggedin)
    sbar = generate_navigation(categories)
    content = generate_login_content(doesregister)
    return generate_hauptlayout(header, sbar, content)

# page /cart?
def generate_warenkorb(loggedin, order_warenkorb, categories):
    header = generate_header(loggedin)
    sbar = generate_navigation(categories)
    content = generate_warenkorb_content(order_warenkorb)
    return generate_hauptlayout(header, sbar, content)

# page /search?category=TEST   & /search?term=TEST 
def generate_searchpage(loggedin, drinks, categories, search_category = False, searchterm = None, category = None):
    header = generate_header(loggedin)
    sbar = generate_navigation(categories)
    if search_category:
        content = generate_search_content(drinks, loggedin)
        return generate_hauptlayout(header, sbar, content)
    content = generate_search_content(drinks, loggedin)
    return generate_hauptlayout(header, sbar, content)

#
#  LEVEL 1
#

def generate_hauptlayout(header, sidebar, content):
    return render_template("Hauptlayout.html", header= header, Sbar= sidebar, content= content)

#
#  LEVEL 2
#
def generate_warenkorb_content(warenkorb):
    s = ""
    for k in warenkorb.order_item_list:
        s += generate_itemslice(k.drink, k.amount)
    return render_template("Warenkorb.html", itemcard=s)

def generate_navigation(categories):
    s = ""
    for k in categories:
        s += generate_nav_category(k)
    return render_template("navigationsleiste.html", category=s)

def generate_login_content(do_register = False):
    if do_register:
        return render_template("Register.html")
    return render_template("Loginp.html")

def generate_header(loggedin):
    searchbar = generate_header_searchbar()
    buttons = generate_header_button(loggedin)
    return render_template("Tleiste.html", Sbar=searchbar, Buttons=buttons)

def generate_search_content(drinks, name):
    cards = ""
    for k in drinks:
        cards += generate_item_card(k)
    return render_template("Search.html", itemcards=cards)

def generate_welcome_content(drinks, loggedin):
    cards = ""
    for k in drinks:
        cards += generate_item_card(k)
    msg = "Logge dich ein um einzukaufen!" 
    if loggedin:
        msg = "Willkommen zurück!"
    return render_template("welcomecon.html", welcomemessage=msg, itemcards=cards)
#
# LEVEL 3
#

def generate_itemslice(drink, quantity):
    return render_template("Itemslice.html", Title=drink.name, Amount=quantity, Preis=drink.price, itemId=drink.id)

def generate_nav_category(category):
    return render_template("category.html", name=category.name, id=category.id)

def generate_header_button(loggedin):
    loginTxt = "Log in / Register"
    loginpth = "/login"
    if loggedin:
        loginTxt = "Log out"
        loginpth = "/logout"
    return render_template("Buttons.html", loginRegisterLogout=loginTxt, loginpath=loginpth)

def generate_header_searchbar():
    return render_template("Sbar.html")

def generate_item_card(drink):
    return render_template("Itemcard.html", Title=drink.name, Bild=str(drink.id), Text=drink.description, Preis=drink.price, itemId=drink.id)