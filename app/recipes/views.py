from flask import Blueprint
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from app.recipes.models import *
from app import app, db
from app.helpers import apology, login_required
from werkzeug.security import check_password_hash, generate_password_hash
import json

mod = Blueprint('recipes', __name__)

from app import UnitsType,CategoryTypeProduct,CategoryTypeRecipes


# retrieve recipe.html
@app.route("/recipes")
@login_required
def recipes():
    products = get_all_products()
    return render_template("/recipes/recipes.html", categories=CategoryTypeRecipes, products=products, units=UnitsType)


# api to get recipes
@app.route('/api/recipes', methods=["GET"])
@login_required
def get_recipes():

    if request.method == "GET":
        try:
            # get all recipes
            recipes = get_sql_recipes(session["user_id"])
        except (RuntimeError, ValueError):
            response = jsonify({'status': 'Recipe cannot be shown'})
            response.status = 404
            return response

        for recipe in recipes:
            try:
                # get ingredients for recipes by recipe id
                ingredients = get_ingredients_to_recipe(recipe["id"])
            except (RuntimeError, ValueError):
                response = jsonify({'status': 'Recipe cannot be shown'})
                response.status = 404
                return response

            recipe["ingredients"] = ingredients

        return {'data': [recipe for recipe in recipes]}


# api to delete recipe
@app.route('/api/recipes', methods=["DELETE"])
@login_required
def delete_recipe():
    ids = ",".join(json.loads(request.data))
    try:
        # delete recipes by ids
        rows = delete_sql_recipes(session["user_id"], ids)
        if rows != len(json.loads(request.data)):
            response = jsonify({'status': 'Some products cannot be deleted'})
            response.status = 404
            return response
    except (RuntimeError, ValueError):
        response = jsonify({'status': 'Recipe cannot be deleted'})
        response.status = 404
        return response

    try:
        # delete ingredients by recipe ids
        rows = delete_ingredients_from_recipe(ids)
    except (RuntimeError, ValueError):
        response = jsonify({'status': 'Recipe cannot be deleted'})
        response.status = 404
        return response

    response = jsonify({'status': 'Ok'})
    response.status = 200
    return response


# api to create recipe
@app.route('/api/recipes', methods=["PUT"])
@login_required
def create_recipe():
    record = json.loads(request.data)
    try:
        id_recipe = create_sql_recipe(session["user_id"], record["name"], record["category"], record["description"])
    except (RuntimeError, ValueError):
        response = jsonify({'status': 'Recipe cannot be created'})
        response.status = 404
        return response

    for product in record["ingredients"]:
        try:
            id_product = get_product_id_by_name(session["user_id"], product["product"])
        except (RuntimeError, ValueError):
            response = jsonify({'status': 'Recipe cannot be created'})
            response.status = 404
            return response

        try:
            # append ingredient for recipe
            rows = add_ingredients_to_recipe(id_recipe, id_product[0]["id"], product["quantity"], product["units"])
        except (RuntimeError, ValueError):
            response = jsonify({'status': 'Recipe cannot be created'})
            response.status = 404
            return response

    response = jsonify({'status': 'Ok'})
    response.status = 200
    return response


# api to cook recipe and remove imgredient from stored products
@app.route('/api/recipes', methods=["POST"])
@login_required
def cook_recipe():
    ids = ",".join(json.loads(request.data))

    try:
        need_for_recipes = get_ingredients_to_recipe(ids)
    except (RuntimeError, ValueError):
        response = jsonify({'status': 'Recipe cannot be cooked'})
        response.status = 404
        return response

    for record in need_for_recipes:
        try:
            rows = update_sql_products(session["user_id"], record["quantity"], record["id"])
            if rows != 1:
                response = jsonify({'status': 'Some products cannot be updated'})
                response.status = 404
                return response
        except (RuntimeError, ValueError):
            response = jsonify({'status': 'Cannot be updated'})
            response.status = 404
            return response

    response = jsonify({'status': 'Ok'})
    response.status = 200
    return response