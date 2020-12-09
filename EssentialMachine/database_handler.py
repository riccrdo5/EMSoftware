import os
import json
import sqlite3
import uuid
from dotenv import load_dotenv

load_dotenv()
db_name = os.environ.get('DB_NAME')
conn = None


def delete_existing_database():
    if os.path.exists(db_name):
        os.remove(db_name)


def create_new_database():
    global conn
    conn = sqlite3.connect(db_name)


def create_tables():
    conn.execute('CREATE TABLE products (product_id TEXT PRIMARY KEY,\
product_name TEXT NOT NULL, unit_price REAL NOT NULL, display_image_path TEXT NOT NULL)')

    conn.execute("CREATE TABLE slots (slot_id TEXT PRIMARY KEY, \
product_id TEXT NOT NULL, quantity INTEGER NOT NULL)")


def read_seed_data(db_seed_file):
    with open(db_seed_file) as f:
        data = json.load(f)
    return data


def insert_to_products_table(cursor, product_id, product):
    cursor.execute('INSERT INTO products (product_id, product_name, unit_price, display_image_path) \
VALUES (?,?,?,?)', (product_id, product["name"], product["unit_price"], product["display_image_path"]))
    conn.commit()


def insert_to_slots_table(cursor, slot_id, product_id, product):
    cursor.execute('INSERT INTO slots (slot_id, product_id, quantity) \
VALUES (?,?,?)', (slot_id, product_id, product["init_quantity"]))
    conn.commit()


def seed_tables(seed_file):
    data = read_seed_data(seed_file)
    cursor = conn.cursor()
    for row in data:
        slot_id, product = row["slot_id"], row["product"]
        product_id = str(uuid.uuid1())
        insert_to_products_table(cursor, product_id, product)
        insert_to_slots_table(cursor, slot_id, product_id, product)
    cursor.close()
    conn.close()


def getProductName():
    global conn
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def get_product_info():
    global conn
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products INNER JOIN slots ON products.product_id = slots.product_id')
    prods = cursor.fetchall()
    cursor.close()
    conn.close()
    return prods


def seed_database(seed_file):
    delete_existing_database()
    create_new_database()
    create_tables()
    seed_tables(seed_file)
