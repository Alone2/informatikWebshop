# https://flask.palletsprojects.com/en/rtd/templating/
from flask import render_template

def generate_homepage(loggedin, categories, drinks):
    return render_template("Hauplayout.html")

def generate_loginpage(loggedin, doesregister, categories, failedMessage = None):
    pass

def generate_warenkorb(loggedin, drinks, categories):
    pass

def generate_searchpage(loggedin, searchterm, drinks, categories):
    pass

def navigation(categories):
    return render_template("Tlesist.html")