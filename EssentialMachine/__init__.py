from flask import Flask, url_for, render_template
from .database_handler import DatabaseHandler

app = Flask(__name__)
#app.config.from_object('config.Config')

#DB_NAME = app.config["DATABASE_NAME"]
#DB_SEED_FILE = app.config["DATABASE_SEED_FILE"]

DB_NAME = "essential_machine.db"
DB_SEED_FILE = "./seed.json"

@app.route('/')
def hello(name=None):
	return render_template('index.html', name=name)

if __name__ == "__main__":
	db_handler = DatabaseHandler(DB_NAME, DB_SEED_FILE)
	db_handler.seed_database()
	app.run()
