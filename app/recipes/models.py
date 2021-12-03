from app import app, db


# get all products
def get_all_products():
    products = db.execute("SELECT products.id , products.name, products.category, products.quantity, products.units FROM products")

    return products


# create recipe
def create_sql_recipe(user_id, name, category, description):
    rows = db.execute("INSERT INTO recipes (id,name,category,description,user_id) VALUES (NULL,:name,:category,:description,:user_id)",
                      description=description, user_id=user_id, name=name, category=category)

    return rows


# get product id by name
def get_product_id_by_name(user_id, name):
    sql_query = "SELECT id FROM products where name='{name}' and user_id={user_id}".format(
                name=name, user_id=user_id)

    rows = db.execute(sql_query)

    return rows


# append ingredients to recipe
def add_ingredients_to_recipe(id_recipe, id_product, quantity, units):
    rows = db.execute("INSERT INTO recipe_to_product (id_recipe,id_product,quantity,units) VALUES\
        		(:id_recipe, :id_product,:quantity,:units)", id_recipe=id_recipe, id_product=id_product, quantity=quantity, units=units)

    return rows


# get details about recipe
def get_sql_recipes(user_id):
    rows = db.execute("SELECT recipes.id , recipes.name, recipes.category, recipes.description FROM recipes \
        					where recipes.user_id = :user_id ", user_id=user_id)

    return rows


# get ingredients for recipe
def get_ingredients_to_recipe(id_recipe):
    sql_query = "SELECT id_product as id, products.name as name, recipe_to_product.quantity,recipe_to_product.units FROM recipe_to_product join products\
     WHERE id_product=products.id and id_recipe in ({id_recipe})".format(id_recipe=id_recipe)
    rows = db.execute(sql_query)

    return rows


# delete recipe
def delete_sql_recipes(user_id, ids):
    sql_query = "DELETE FROM recipes WHERE id in ( {ids} ) and user_id = {user_id}".format(ids=ids, user_id=user_id)

    rows = db.execute(sql_query)
    return rows


# delete ingredients for recipe
def delete_ingredients_from_recipe(ids):
    sql_query = "DELETE FROM recipe_to_product WHERE id_recipe in ( {ids} )".format(ids=ids)

    rows = db.execute(sql_query)
    return rows


# remove quantity of product that need to cook recipes
def update_sql_products(user_id, quantity, id):
    sql_request = "UPDATE products SET quantity=quantity-{quantity} WHERE id={id} and user_id={user_id}".format(
        user_id=user_id, quantity=quantity, id=id)

    rows = db.execute(sql_request)
    return rows