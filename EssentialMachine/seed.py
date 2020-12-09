from database_handler import  seed_database

DB_NAME = "essential_machine.db"
DB_SEED_FILE = "./seed.json"

seed_database(DB_SEED_FILE)