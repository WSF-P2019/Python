from flask import Blueprint, jsonify, request
from helpers.payment_helper import payment_helper
from helpers.user_helper import user_helper
from helpers.token_helper import token_helper
from models import Payment
from models import User
from models import Token
from playhouse.shortcuts import model_to_dict, dict_to_model

app_payment = Blueprint('app_payment', __name__)

@app_payment.route('/user/<name>/transactions', methods=['GET'])
def get_all_user_payment(name):
    pass

@app_payment.route('/user/<name>/transactions', methods=['POST'])
def add_user_payment(name):
    pass

@app_payment.route('/user/<nameid>/transactions', methods=['PUT'])
def update_user_payment(name):
    pass

@app_payment.route('/user/<name>/transactions', methods=['DELETE'])
def delete_user_payment(name):
    pass

# @app_payment.route('/user/<name>/transaction/<id>', methods=['GET'])
# @app_payment.route('/user/<name>/transaction/<id>', methods=['POST'])
# @app_payment.route('/user/<name>/transaction/<id>', methods=['PUT'])
# @app_payment.route('/user/<name>/transaction/<id>', methods=['DELETE'])