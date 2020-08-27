# https://flask.palletsprojects.com/en/rtd/templating/
from flask import render_template

# page /
def generate_homepage(loggedin, categories, drinks, failedMessage = None):
    return render_template("Hauplayout.html")

# page /login and /register
def generate_loginpage(loggedin, doesregister, categories, failedMessage = None):
    pass

# page /cart?
def generate_warenkorb(loggedin, drinks, categories):
    pass

# page /search?category=TEST   & /search?term=TEST 
def generate_searchpage(loggedin, drinks, categories, search_category = False, searchterm = None, category = None):
    pass

def navigation(categories):
    s = ""
    for k in categories:
        s += category(k)
    return render_template("navigationsleiste.html", category=s)

def category(category):
    return render_template("category.html", name=category.name)