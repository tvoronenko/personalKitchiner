from app import app, db


# create product
def create_sql_product(user_id, name, units, quantity, category):
    rows = db.execute("INSERT INTO products (id,name,units,quantity,user_id,category) VALUES\
    			(NULL,:name,:units, :quantity,:user_id,:category)", name=name, units=units, quantity=quantity, user_id=user_id, category=category)

    return rows


# get all produts
def get_all_products(user_id):
    products = db.execute("SELECT products.id , products.name, products.category, products.quantity, products.units FROM products \
        					where products.user_id = :user_id and products.quantity > 0", user_id=user_id)

    return products


# delete product by set quantity to 0
def delete_sql_products(user_id, data):
    ids = ",".join(data)
    sql_query = "UPDATE products SET quantity=0 WHERE id in ( {ids} ) and user_id = {user_id}".format(
        ids=ids, user_id=user_id)
    rows = db.execute(sql_query)

    return rows


# update quantity
def update_sql_products(type_request, user_id, quantity, id):
    if type_request == "add":
        sql_request = "UPDATE products SET quantity=quantity+{quantity} WHERE id={id} and user_id={user_id}".format(
            user_id=user_id, quantity=quantity, id=id)
    else:
        sql_request = "UPDATE products SET quantity={quantity} WHERE id={id} and user_id={user_id}".format(
            user_id=user_id, quantity=quantity, id=id)

    rows = db.execute(sql_request)
    return rows