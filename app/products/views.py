from flask import Blueprint
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from app.products.models import *
from app import app, db
from app.helpers import apology, login_required
from werkzeug.security import check_password_hash, generate_password_hash
import json

mod = Blueprint('products', __name__)

from app import UnitsType,CategoryTypeProduct


# retrive product.html and home page
@app.route("/")
@login_required
def index():
    return render_template("/products/products.html", categories=CategoryTypeProduct, units=UnitsType)


# api to create product
@app.route('/api/products', methods=["PUT"])
def create_products():
    record = json.loads(request.data)

    try:
        res = create_sql_product(session["user_id"], record["name"], record["units"], record["quantity"], record["category"])
    except (RuntimeError, ValueError):
        response = jsonify({'status': 'Cannot be added'})
        response.status = 400
        return response
    response = jsonify({'status': 'Ok'})
    response.status = 200
    return response


# api to delete product by setting quantity to 0
@app.route('/api/products', methods=["DELETE"])
def delete_products():
    try:
        rows = delete_sql_products(session["user_id"], json.loads(request.data))

        if rows != len(json.loads(request.data)):
            response = jsonify({'status': 'Some products cannot be deleted'})
            response.status = 404
            return response
    except (RuntimeError, ValueError):
        response = jsonify({'status': 'Cannot be deleted'})
        response.status = 404
        return response
    response = jsonify({'status': 'Ok'})
    response.status_code = 200
    return response


# api to update quantity
@app.route('/api/products', methods=["POST"])
def update_products():
    if request.method == "POST":
        responce_data = json.loads(request.data)
        type_request = responce_data["type"]
        records = responce_data["data"]
        for record in records:
            try:
                rows = update_sql_products(type_request, session["user_id"], record["quantity"], record["id"])
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


# api to get products
@app.route('/api/products', methods=["GET"])
def get_products():
    if request.method == "GET":
        try:
            products = get_all_products(session["user_id"])
        except (RuntimeError, ValueError):
            response = jsonify({'status': 'Products cannot be shown'})
            response.status = 400
            return response
        return {'data': [product for product in products]}

