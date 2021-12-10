from app import db


def create_table_users():
    sql_query = "CREATE TABLE users (id integer PRIMARY KEY AUTOINCREMENT,\
    username text, hash text);"
    res = db.execute(sql_query)
    return res


def create_table_products():
    sql_query = "CREATE TABLE products (\
    id integer PRIMARY KEY AUTOINCREMENT NOT NULL,\
    name text,\
    units text,\
    quantity int,\
    user_id int,\
    category text);"
    res = db.execute(sql_query)
    return res


def create_table_recipes():
    sql_query = "CREATE TABLE recipes (\
    id integer PRIMARY KEY AUTOINCREMENT NOT NULL,\
    name text,\
    description text,\
    user_id int,\
    category text);"
    res = db.execute(sql_query)
    return res


def create_table_recipe_to_product():
    sql_query = "CREATE TABLE recipe_to_product (\
    id_recipe integer ,\
    id_product integer,\
    quantity int,\
    units text);"
    res = db.execute(sql_query)
    return res


def drop_table(name_table):
    sql_query = "DROP TABLE " + name_table
    res = db.execute(sql_query)
    return res


def create_user():
    sql_query = "INSERT  INTO users(username, hash)  VALUES('test', 'pbkdf2:sha256:150000$pStajWoh$80e9c18f3bc1350a045d1ab1a7b163f363f1625595d7c5efe00bfe31c5ff133f');"
    res = db.execute(sql_query)
    return res


def delete_from_table(name_table):
    sql_query = "DELETE FROM " + name_table
    res = db.execute(sql_query)
    return res