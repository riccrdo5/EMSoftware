from database_handler import DatabaseHandler

DB_NAME = "essential_machine.db"
DB_SEED_FILE = "./seed.json"

db_handler = DatabaseHandler(DB_NAME, DB_SEED_FILE)
db_handler.seed_database()