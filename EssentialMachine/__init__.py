import base64
import json
import os
import shlex
import subprocess
from gpiozero import LED
from time import sleep

import braintree
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

from . import database_handler

load_dotenv(dotenv_path='//var//www//Essential-Machine//EssentialMachine//.env')

app = Flask(__name__)
TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]

led_mapping = {
    'Surgical Face Mask': 17,
    'Disposable Nitrile': 18,
    '3.4 fl oz Bottle Sanitizer': 22
}


def blinkLed(prod_list):
    # need a prod to led port
    for prod in prod_list:
        if prod.get('Product(s)') in led_mapping:
            led = LED(led_mapping[prod.get('Product(s)')])
            for i in range(int(prod.get('Quantity'))):
                # print("blinking " + prod.get('Product Name'))
                led.on()
                sleep(0.5)
                led.off()
                sleep(0.5)

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


def validatePurchaseRequest(prod_list):
    products = get_products()
    success = True
    # verify product name, price and quantity
    for purchased_prod in prod_list:
        db_prod = next((x for x in products if x.name == purchased_prod.get('Product(s)')), None)
        if db_prod is None:
            success = False
            break
        else:
            if float(purchased_prod.get('Price')) != float(db_prod.price):
                success = False
                break
            else:
                if int(purchased_prod.get('Quantity')) > int(db_prod.maxqty):
                    success = False
                    break
    return success


@app.route('/purchase', methods=['POST'])
def purchase(name=None):
    json_data = request.json
    prod_list = json_data.get('prods')
    success = validatePurchaseRequest(prod_list)
    if not success:
        response = jsonify(msg='Something went wrong')
        return response, 500

    payment_nonce = json_data.get('nonce')
    amount = 0.0
    for prod in prod_list:
        amount += float(prod.get('Price')) * int(prod.get('Quantity'))
        amount = round(amount, 2)
    result = gateway.transaction.sale({
        'amount': str(amount),
        'payment_method_nonce': payment_nonce,
        'options': {
            "submit_for_settlement": True
        }
    })
    if result.is_success or result.transaction:
        # logTransaction(amount)
        blinkLed(prod_list)
        response = jsonify(transaction_id=result.transaction.id, prods=prod_list)
        return response
    else:
        response = jsonify(msg='Something went wrong')
        return response, 500


def find_transaction(id):
    return gateway.transaction.find(id)


if __name__ == "__main__":
    app.run()
