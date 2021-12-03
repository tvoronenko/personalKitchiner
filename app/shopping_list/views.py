from flask import Blueprint
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from app.shopping_list.models import *
from app import app, db
from app.helpers import apology, login_required
from werkzeug.security import check_password_hash, generate_password_hash
import json


# register this view
mod = Blueprint('shopping_list', __name__)

from app import UnitsType,CategoryTypeProduct,CategoryRecipes


# load shopping_list page
@app.route("/shopping_list")
@login_required
def shopping_list():
    return render_template("/shopping_list/shopping_list.html")


# api for getting ingredients for selected recipes
@app.route('/api/shopping_list', methods=["GET"])
@login_required
def get_shopping_list():
    ids = request.args.get("ids")
    if ids != "":
        ids = request.args.get("ids").split("=")[1]
        try:
            # get  all ingredoents for all recipes
            need_for_recipes = get_ingrediets_to_recipes(ids)
        except (RuntimeError, ValueError):
            response = jsonify({'status': 'Shopping list cannot be created'})
            response.status = 404
            return response

        # get  id of ingredients in flat list
        ids_nested = [[t for v, t in k.items() if v == "id"] for k in need_for_recipes]
        ids_flat = [str(i) for sublist in ids_nested for i in sublist]
        ids = ",".join(ids_flat)

        try:
            # get quantity products in storage
            products = get_details_about_products(session["user_id"], ids)
        except (RuntimeError, ValueError):
            response = jsonify({'status': 'Shopping list cannot be created'})
            response.status = 404
            return response
        product_dict = {}
        for product in products:
            product_dict[product["id"]] = product["quantity"]

        # determine how many products need to buy
        need_to_buy = []
        for ingred in need_for_recipes:
            if (product_dict[ingred["id"]] - ingred["quantity"]) < 0:
                need_to_buy.append(ingred)

        return {'data': [product for product in need_to_buy]}
    else:
        return {'data': []}