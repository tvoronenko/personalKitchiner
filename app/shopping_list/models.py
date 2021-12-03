from app import app, db


# get ingredients for recipes
def get_ingrediets_to_recipes(ids):

    sql_query = "SELECT id_product as id,name,sum(recipe_to_product.quantity) as quantity, category, recipe_to_product.units FROM recipe_to_product join products on products.id=recipe_to_product.id_product\
        WHERE id_recipe in ( {ids}) group by id_product".format(ids=ids)
    rows = db.execute(sql_query)

    return rows


# get details about stored products
def get_details_about_products(user_id, ids):

    sql_query = "SELECT products.id ,products.quantity FROM products \
                            where products.user_id = {user_id} and  products.id in ({ids})".format(user_id=user_id, ids=ids)
    rows = db.execute(sql_query)

    return rows