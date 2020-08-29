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
    pass

# page /cart?
def generate_warenkorb(loggedin, drinks, categories):
    pass

# page /search?category=TEST   & /search?term=TEST 
def generate_searchpage(loggedin, drinks, categories, search_category = False, searchterm = None, category = None):
    pass

#
#  LEVEL 1
#

def generate_hauptlayout(header, sidebar, content):
    return render_template("Hauptlayout.html", header= header, Sbar= sidebar, content= content)

#
#  LEVEL 2
#

def generate_navigation(categories):
    s = ""
    for k in categories:
        s += generate_nav_category(k)
    return render_template("navigationsleiste.html", category=s)


def generate_header(loggedin):
    searchbar = generate_header_searchbar()
    buttons = generate_header_button(loggedin)
    return render_template("Tleiste.html", Sbar=searchbar, Buttons=buttons)

def generate_welcome_content(drinks, loggedin):
    cards = ""
    for k in drinks:
        cards += generate_item_card(k.name, "/img?item="+str(k.id), k.description, k.price)
    msg = "Please log in" 
    if loggedin:
        msg = "Welcome back!"
    return render_template("welcomecon.html", welcomemessage=msg, itemcards=cards)
#
# LEVEL 3
#

def generate_nav_category(category):
    return render_template("category.html", name=category.name, id=category.id)

def generate_header_button(loggedin):
    loginTxt = "Log in / Register"
    if loggedin:
        loginTxt = "Log out"
    return render_template("Buttons.html", loginRegisterLogout=loginTxt)

def generate_header_searchbar():
    return render_template("Sbar.html")

def generate_item_card(title, imagesrc, description, price):
    return render_template("Itemcard.html", Title=title, Bild=imagesrc, Text=description, Preis=price)