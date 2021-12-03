import os
import enum
from flask import Blueprint
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

import json
from app.helpers import apology, login_required

class CategoryProduct(enum.Enum):
    vegetable = 1
    milk = 2
    meat = 3
    spice = 4
    fruits = 5


CategoryTypeProduct = {}
CategoryTypeProduct[CategoryProduct.vegetable] = "vegetable"
CategoryTypeProduct[CategoryProduct.milk] = "milk product"
CategoryTypeProduct[CategoryProduct.meat] = "meat"
CategoryTypeProduct[CategoryProduct.spice] = "spice"
CategoryTypeProduct[CategoryProduct.fruits] = "fruits"


class CategoryRecipes(enum.Enum):
    breaskfast = 1
    lunch = 2
    dinner = 3
    brunch = 4
    appetizer = 5
    salad = 6


CategoryTypeRecipes = {}
CategoryTypeRecipes[CategoryRecipes.breaskfast] = "breaskfast"
CategoryTypeRecipes[CategoryRecipes.lunch] = "lunch"
CategoryTypeRecipes[CategoryRecipes.dinner] = "dinner"
CategoryTypeRecipes[CategoryRecipes.brunch] = "brunch"
CategoryTypeRecipes[CategoryRecipes.appetizer] = "appetizer"
CategoryTypeRecipes[CategoryRecipes.salad] = "salad"


class Units(enum.Enum):
    oz = 1
    tsp = 2
    tbsp = 3
    ea = 4


UnitsType = {}
UnitsType[Units.ea] = "ea"
UnitsType[Units.tsp] = "tsp"
UnitsType[Units.tbsp] = "tbsp"
UnitsType[Units.ea] = "ea"

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

env_var = "FLASK_ENV"
if env_var in os.environ:
    if os.environ[env_var] == "development":
        app.config.from_object('config.DebugConfiguration')
        db = SQL(app.config['DATABASE_URI'])
    else:
        app.config.from_object('config.TestConfiguration')
        db = SQL(app.config['DATABASE_URI'])
else:
    app.config.from_object('config.DebugConfiguration')
    db = SQL(app.config['DATABASE_URI'])


from app.auth.views import mod as authModule
app.register_blueprint(authModule)

from app.products.views import mod as productsModule
app.register_blueprint(productsModule)

from app.recipes.views import mod as recipesModule
app.register_blueprint(recipesModule)

from app.shopping_list.views import mod as shopping_listModule
app.register_blueprint(shopping_listModule)

#----------------------------------------
# controllers
#----------------------------------------


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
