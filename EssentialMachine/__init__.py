from flask import Flask, url_for, render_template
from .database_handler import DatabaseHandler

app = Flask(__name__)
# app.config.from_object('config.Config')

# DB_NAME = app.config["DATABASE_NAME"]
# DB_SEED_FILE = app.config["DATABASE_SEED_FILE"]

@app.route('/')
def hello(name=None):
    return render_template('index.html', name=name)


@app.route('/billing_summary')
def billing_summary(name=None):
    return render_template('billing_summary.html', name=name)

if __name__ == "__main__":
    app.run()
