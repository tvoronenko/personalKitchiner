import enum
from flask import redirect, render_template, request, session
from functools import wraps


def load_type_product():
    import csv

    filename = "category_products.csv"
    category = {}
    # opening the file using "with"
    # statement
    with open(filename, 'r') as data:
        for line in csv.DictReader(data):
            category[line["key"]] = line["value"]
    return category


def load_units():
    import csv

    filename = "units.csv"
    units = {}
    # opening the file using "with"
    # statement
    with open(filename, 'r') as data:
        for line in csv.DictReader(data):
            units[line["key"]] = line["value"]
    return units


def load_type_recipe():
    import csv

    filename = "category_recipes.csv"
    category = {}
    # opening the file using "with"
    # statement
    with open(filename, 'r') as data:
        for line in csv.DictReader(data):
            category[line["key"]] = line["value"]
    return category


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("/error/apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
