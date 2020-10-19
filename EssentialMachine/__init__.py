from flask import Flask, url_for, render_template
from database_handler import DatabaseHandler

app = Flask(__name__)
# app.config.from_object('config.Config')

# DB_NAME = app.config["DATABASE_NAME"]
# DB_SEED_FILE = app.config["DATABASE_SEED_FILE"]

DB_NAME = "essential_machine.db"
DB_SEED_FILE = "./seed.json"

class Product():
    id = 0
    name = ""
    price = 0
    img_path = ""
    
    def __repr__(self):
        return 'Item %r' % self.id

@app.route('/')
def hello(name=None):
    return render_template('index.html', name=name)


@app.route('/billing_summary')
def billing_summary(name=None):
    return render_template('billing_summary.html', name=name)


@app.route('/cart')
def cart(name=None):
    prods = db_handler.getProductName()
    products = []
    for prod in prods:
        currProd = Product()
        currProd.id = prod[0]
        currProd.name = prod[1]
        currProd.price = prod[2]
        currProd.img_path = prod[3]
        products.append(currProd)

    # print(products)
    return render_template('cart.html', products = products)


if __name__ == "__main__":
    db_handler = DatabaseHandler(DB_NAME, DB_SEED_FILE)
    db_handler.seed_database()
    app.run()
