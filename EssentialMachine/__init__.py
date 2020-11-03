import braintree
import os
import shlex
import subprocess
from flask import Flask, url_for, render_template, request, redirect, flash
from database_handler import DatabaseHandler


app = Flask(__name__)
# app.config.from_object('config.Config')

# DB_NAME = app.config["DATABASE_NAME"]
# DB_SEED_FILE = app.config["DATABASE_SEED_FILE"]

DB_NAME = "essential_machine.db"
DB_SEED_FILE = "./seed.json"

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
    price = 0
    img_path = ""
    
    def __repr__(self):
        return 'Item %r' % self.id

@app.route('/')
def hello(name=None):
    return render_template('index.html', name=name)


@app.route('/checkouts/<transaction_id>', methods=['GET'])
def show_checkout(transaction_id):
    transaction = find_transaction(transaction_id)
    result = {}
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

    return render_template('show.html', transaction=transaction, result=result)


def logTransaction(request):
    subprocess.call(shlex.split('./test.sh ' + request.form['amount']))


@app.route('/purchase', methods=['POST'])
def purchase(name=None):
    result = gateway.transaction.sale({
        'amount': request.form['amount'],
        'payment_method_nonce': request.form['payment_method_nonce'],
        'options': {
            "submit_for_settlement": True
        }
    })
    if result.is_success or result.transaction:
        logTransaction(request)
        return redirect(url_for('show_checkout',transaction_id=result.transaction.id))
    else:
        for x in result.errors.deep_errors: flash('Error: %s: %s' % (x.code, x.message))
        return redirect(url_for('new_checkout'))

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

def find_transaction(id):
    return gateway.transaction.find(id)

if __name__ == "__main__":
    db_handler = DatabaseHandler(DB_NAME, DB_SEED_FILE)
    db_handler.seed_database()
    app.run(host='10.3.15.154')
