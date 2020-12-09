import braintree
import base64
import shlex
import json
import subprocess
from flask import Flask, render_template, request, jsonify
#from gpiozero import LED
from time import sleep
import database_handler
import sqlite3

app = Flask(__name__)
# app.config.from_object('config.Config')

# DB_NAME = app.config["DATABASE_NAME"]
# DB_SEED_FILE = app.config["DATABASE_SEED_FILE"]

#DB_NAME = "essential_machine.db"
#DB_SEED_FILE = "./seed.json"

TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        environment='sandbox',
        merchant_id='vtj2pcb46ytpj78b',
        public_key='hvfxn5555z682fhp',
        private_key='0744c74eca323071709af48de8241f5c'
    )
)



class Product():
    id = 0
    name = ""
    price = ""
    img_path = ""
    
    def __repr__(self):
        return 'Item %r' % self.id

@app.route('/')
def cart(name=None):
    conn = sqlite3.connect('essential_machine.db')
    cursor = conn.cursor()
    #cursor.execute('SELECT * FROM products')
    #prods = cursor.fetchall()
    cursor.execute('SELECT * FROM products INNER JOIN slots ON products.product_id = slots.product_id')
    prods = cursor.fetchall()
    cursor.close()
    conn.close()
    products = []
    for prod in prods:
        currProd = Product()
        currProd.id = prod[0]
        currProd.name = prod[1]
        currProd.price = "{:.2f}".format(prod[2])
        #print('price = '+currProd.price)
        currProd.img_path = prod[3]
        currProd.maxqty = prod[6]
        products.append(currProd)
        
    return render_template('index.html', products = products)


@app.route('/fail')
def show_failure(name=None):
    print("something failed")
    return render_template('fail.html', name=name)

@app.route('/checkouts/<transaction_id>', methods=['GET'])
def show_checkout(transaction_id):
    prods = request.args.get('data', default='', type=str)
    prod_string = base64.b64decode(prods)
    prod_json = json.loads(prod_string)
    total = 0.0
    for prod in prod_json:
        total += float(prod['Total'])
    transaction = find_transaction(transaction_id)
    if transaction.status in TRANSACTION_SUCCESS_STATUSES:
        result = {
            'header': 'Success!',
            'icon': 'success',
            'message': 'Your test transaction has been successfully processed.'
        }
    else:
        result = {
            'header': 'Transaction Failed',
            'icon': 'fail',
            'message': 'Your test transaction has a status of ' + transaction.status + '. See the Braintree API response and try again.'
        }

    return render_template('show.html', prods=prod_json, result=result, total=total)


def logTransaction(amount):
    subprocess.call(shlex.split('./test.sh ' + str(amount)))

@app.route('/purchase', methods=['POST'])
def purchase(name=None):
    json_data = request.json
    prod_list = json_data.get('prods')
    payment_nonce = json_data.get('nonce')
    amount = 0.0
    for prod in prod_list:
        amount += float(prod.get('Total'))
    result = gateway.transaction.sale({
        #'amount': request.form['amount'],
        'amount': str(amount),
        'payment_method_nonce': payment_nonce,
        'options': {
            "submit_for_settlement": True
        }
    })
    print(result)
    if result.is_success or result.transaction:
        logTransaction(amount)
        #blinkLed()
        response = jsonify(transaction_id=result.transaction.id, prods = prod_list)
        return response
    else:
        response = jsonify(msg = 'Something went wrong')
        return response, 500

def find_transaction(id):
    return gateway.transaction.find(id)

if __name__ == "__main__":
    app.run()
