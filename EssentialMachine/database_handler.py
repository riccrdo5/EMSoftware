import os
import json
import sqlite3
import uuid 

class DatabaseHandler:
	''' Handles all Database related operations'''
	
	def __init__(self, db_name, db_seed_file):
		self.db_name = db_name
		self.db_seed_file = db_seed_file
		self.conn = None

	def delete_existing_database(self):
		if(os.path.exists(self.db_name)):
			os.remove(self.db_name)

	def create_new_database(self):
		self.conn = sqlite3.connect(self.db_name)
		
	def create_tables(self):
		self.conn.execute('CREATE TABLE products (product_id TEXT PRIMARY KEY,\
		 product_name TEXT NOT NULL, unit_price REAL NOT NULL, display_image_path TEXT NOT NULL)')

		self.conn.execute('CREATE TABLE slots (slot_id TEXT PRIMARY KEY, \
			product_id TEXT NOT NULL, quantity INTEGER NOT NULL)')
		
	def read_seed_data(self):
		with open(self.db_seed_file) as f:
			data = json.load(f)
		return data

	def insert_to_products_table(self, cursor, product_id, product):
		cursor.execute('INSERT INTO products (product_id, product_name, unit_price, display_image_path) \
			VALUES (?,?,?,?)', (product_id, product["name"], product["unit_price"], product["display_image_path"]))
		self.conn.commit()

	def insert_to_slots_table(self, cursor, slot_id, product_id, product):
		cursor.execute('INSERT INTO slots (slot_id, product_id, quantity) \
			VALUES (?,?,?)', (slot_id, product_id, product["init_quantity"]))
		self.conn.commit()

	def seed_tables(self):
		data = self.read_seed_data()
		cursor = self.conn.cursor()
		for row in data:
			slot_id, product = row["slot_id"], row["product"]
			product_id = str(uuid.uuid1())
			self.insert_to_products_table(cursor, product_id, product)
			self.insert_to_slots_table(cursor, slot_id, product_id, product)
		cursor.close()
		self.conn.close()

	def seed_database(self):
		self.delete_existing_database()
		self.create_new_database()
		self.create_tables()
		self.seed_tables()



	
