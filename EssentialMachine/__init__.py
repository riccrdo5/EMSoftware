import base64
import json
import os
import shlex
import subprocess
import sqlite3
import logging
from . import led

import braintree
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

from . import database_handler


load_dotenv(dotenv_path='//var//www//Essential-Machine//EssentialMachine//.env')


app = Flask(__name__)
app.logger.setLevel(logging.INFO)
TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]

"""Venmo gateway setup. Takes values from .env file
    For more information about venmo setup, visit: https://developers.braintreepayments.com/guides/venmo/overview
"""
gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        environment=os.environ.get('BT_ENVIRONMENT'),
        merchant_id=os.environ.get('BT_MERCHANT_ID'),
        public_key=os.environ.get('BT_PUBLIC_KEY'),
        private_key=os.environ.get('BT_PRIVATE_KEY')
    )
)


class Product:
    id = 0
    name = ""
    price = ""
    img_path = ""

    def __repr__(self):
        return 'Item %r' % self.id

#Gets product listing from database
def get_products():
    prods = database_handler.get_product_info()
    products = []
    for prod in prods:
        curr_prod = Product()
        curr_prod.id = prod[0]
        curr_prod.name = prod[1]
        curr_prod.price = "{:.2f}".format(prod[2])
        curr_prod.img_path = prod[3]
        curr_prod.maxqty = prod[6]
        products.append(curr_prod)
    return products


@app.route('/')
def cart(name=None):
    return render_template('index.html', products=get_products())


@app.route('/fail')
def show_failure(name=None):
    app.logger.error("something failed")
    return render_template('fail.html', name=name)

#Returns success if transaction with <transaction_id> is successful
@app.route('/checkouts/<transaction_id>', methods=['GET'])
def show_checkout(transaction_id):
    prods = request.args.get('data', default='', type=str)
    prod_string = base64.b64decode(prods)
    prod_json = json.loads(prod_string)
    total = 0.0
    for prod in prod_json:
        total += float(prod['Total'][1:])
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

# verify product name, price and quantity for purchase request
def validatePurchaseRequest(prod_list, products):
    success = True
    for purchased_prod in prod_list:
        db_prod = next((x for x in products if x.name == purchased_prod.get('Product(s)')), None)
        if db_prod is None:
            success = False
            app.logger.error("Could not find product in database")
            break
        else:
            if float(purchased_prod.get('Price')[1:]) != float(db_prod.price):
                success = False
                app.logger.error('Price mismatch')
                break
            else:
                if int(purchased_prod.get('Quantity')) > int(db_prod.maxqty):
                    success = False
                    app.logger.error('Quantity specified is greater than available quantity')
                    break
    return success

#Updates product quantities in the database after the purchase
def update_prod_quantities(prod_list, db_products):
    conn = sqlite3.connect(os.environ.get('DB_NAME'))
    for prod in prod_list:
        db_prod = next((x for x in db_products if x.name == prod.get('Product(s)')), None)
        new_quantity = int(db_prod.maxqty) - int(prod.get('Quantity'))
        database_handler.update_prod_quantity(conn, db_prod.id, new_quantity)
    conn.commit()
    conn.close()


@app.route('/purchase', methods=['POST'])
def purchase():
    app.logger.info('purchase request : %s', request.json)
    json_data = request.json
    prod_list = json_data.get('prods')
    db_products = get_products()
    success = validatePurchaseRequest(prod_list, db_products)
    if not success:
        response = jsonify(msg='Something went wrong')
        return response, 500
    #Need to send this nonce to venmo servers
    payment_nonce = json_data.get('nonce')
    amount = 0.0
    for prod in prod_list:
        amount += float(prod.get('Price')[1:]) * int(prod.get('Quantity'))
        amount = round(amount, 2)
    result = gateway.transaction.sale({
        'amount': str(amount),
        'payment_method_nonce': payment_nonce,
        'options': {
            "submit_for_settlement": True
        }
    })

    app.logger.info('Transaction submitted to Venmo. result : %s', result)
    if result.is_success or result.transaction:
        led.blinkLed(prod_list)
        update_prod_quantities(prod_list, db_products)
        response = jsonify(transaction_id=result.transaction.id, prods=prod_list)
        return response
    else:
        app.logger.error('Transaction failed. Transaction id: %s, amount: %s', result.transaction.id, str(amount))
        response = jsonify(msg='Something went wrong')
        return response, 500


def find_transaction(id):
    return gateway.transaction.find(id)

#Entry point for the app
if __name__ == "__main__":
    app.run()
