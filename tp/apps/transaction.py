import os,binascii
import time
from flask import Blueprint, jsonify, request
from helpers.transaction_helper import transaction_helper
from helpers.user_helper import user_helper
from helpers.token_helper import token_helper
from models import Transaction
from models import User
from models import Token
from models import BuyCode
from playhouse.shortcuts import model_to_dict, dict_to_model

import stripe
stripe.api_key = "sk_test_???"

import nexmo
client = nexmo.Client(key='???"', secret='???"')

app_transaction = Blueprint('app_transaction', __name__)

def logged_checker(token):
 try:
   token = Token.get(Token.token == token)
   currentTime = int(time.time())
   if (currentTime < token.expiration_date):
     return token
   else:
     return False
 except Exception as error:
   return False

def user_checker(Token, Transaction):
 if Token.user_id == Transaction.user_id:
   return True
 else:
   return False

# Charge the user's card:
@app_transaction.route('/buy', methods=['POST'])
def buy_something():
    params = request.get_json()
    token = logged_checker(params.get('token'))
    if token is False:
        return jsonify({'error':'Token expired, please update it on /tokens/update/<id> '})
    card = {
        'number': params.get('number'),
        'exp_month': params.get('exp_month'),
        'exp_year': params.get('exp_year'),
        'cvc': params.get('cvc')
    }
    user = User.get(User.id == token.user_id)
    source = stripe.Token.create(card=card)
    try:
        charge = stripe.Charge.create(
            amount=params.get('amount'),
            currency="usd",
            card=source.id,
            capture=False,
            description="Example charge"
        )
        generatedMobileCode = binascii.b2a_hex(os.urandom(2))
        client.send_message({
          'from': 'Buy - Python TP',
          'to': user.phone_number,
          'text': generatedMobileCode,
        })
        code = BuyCode.create(user_id=user.id, buy_code=generatedMobileCode, charge_id=charge.id, amount=charge.amount)
        code.save()
        codeData = model_to_dict(code)
        return jsonify({'response': 'Payement well captured and BuyCode well registered', 'code': codeData}), 201
    except Exception as identifier:
        return jsonify({'error': 'Payement issue {message}.'.format(message=identifier.message)}), 404

@app_transaction.route('/buy/validate', methods=['POST'])
def buy_validate():
    params = request.get_json()
    paramsToken = logged_checker(params.get('token'))
    paramsCode = params.get('code')
    if paramsToken is False:
        return jsonify({'error':'Token expired, please update it on /tokens/update/<id> '})
    else:
        try:
            code = BuyCode.get(BuyCode.buy_code == paramsCode)
            if code.buy_code == paramsCode:
                charge = stripe.Charge.retrieve(code.charge_id)
                charge.capture()

                transaction = Transaction.create(user_id=code.user_id, amount=charge.amount, bank='Stripe')
                transaction.save()
                transactionData = model_to_dict(transaction)
                return jsonify({'response': 'Payement worked and transaction well registered in DB', 'transaction': transactionData}), 201
            return str('Code given did not match to code generated')
        except Exception as identifier:
            return jsonify({'error': '{message}'.format(message=identifier.message)}), 404

@app_transaction.route('/transactions', methods=['POST'])
def create_transaction():
    # Get the token in the parameters
    params = request.get_json()
    paramsToken = params.get('token')
    paramsAmount = params.get('amount')
    paramsBank = params.get('bank')

    # Check if the token exist
    try:
        token = Token.get(Token.token == paramsToken)
        if time.time() < token.expiration_date:
            transaction = Transaction.create(user_id=token.user_id, amount=paramsAmount, bank=paramsBank)
            transaction.save()
            transactionData = model_to_dict(transaction)
            return jsonify({'response': 'Transaction well created', 'transaction': transactionData}), 201
        else:
            return str('Your token is expired. Please update it by login again on: /tokens/update/<id>.')
    except Exception as identifier:
        return jsonify({'error': 'Token not found {message}'.format(message=identifier.message)}), 404

@app_transaction.route('/transactions/find', methods=['POST'])
def get_transactions():
    # Get the token in the parameters
    params = request.get_json()
    paramsToken = params.get('token')

     # Check if the token exist
    try:
        token = Token.get(Token.token == paramsToken)
        if time.time() < token.expiration_date:
            transactions = list(Transaction.select().where(Transaction.user_id == token.user_id).dicts())
            return jsonify({'transactions': transactions}), 201
        else:
            return str('Your token is expired. Please delete this one, and create another one.')
    except Exception as identifier:
        return jsonify({'error': 'Token not found {message}'.format(message=identifier.message)}), 404

@app_transaction.route('/transactions/<id>', methods=['DELETE'])
def delete_transaction(id):
    # Get the token in the parameters
    params = request.get_json()
    paramsToken = params.get('token')

    # Check if the token exist
    try:
        token = Token.get(Token.token == paramsToken)
        if time.time() < token.expiration_date:
            transaction =  Transaction.get(Transaction.id == id)
            if transaction.user_id == token.user_id:
                is_deleted = transaction.delete_instance()
                return str(is_deleted)
            else:
                return str('The token is not matching with the user_id of the specific transaction')
        else:
            return str('Your token is expired. Please delete this one, and create another one.')
    except Exception as identifier:
        return jsonify({'error': 'Token not found {message}'.format(message=identifier.message)}), 404
