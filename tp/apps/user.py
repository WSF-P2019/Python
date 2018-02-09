import os,binascii
import hashlib
from flask import Blueprint, jsonify, request
from helpers.user_helper import user_helper
from models import User
from playhouse.shortcuts import model_to_dict, dict_to_model

import stripe
stripe.api_key = "sk_test_???""

app_user = Blueprint('app_user', __name__)

# Get all our users
@app_user.route('/users', methods=['GET'])
def get_users():
    return jsonify({'users': list(User.select().dicts()) }), 201

# Create a new user
@app_user.route('/users', methods=['POST'])
def create_user():
    # Let's get the request
    params = request.get_json()
    name = params.get('name')
    password = params.get('password')
    phone_number = params.get('phone_number')
    password_hashed = hashlib.md5(password).hexdigest()
    customer = stripe.Customer.create(
        email=name,
        description='test customer'
    )
    # Then we create the user, and save it in the db
    user = User.create(name=name, password=password_hashed, phone_number=phone_number, stripe_id=customer.id)
    user.save()
    # We convert our model(user) to a dict
    data = model_to_dict(user)
    # Then we send the informations into JSON
    return jsonify({'user': data}), 201

# Get a specific user
@app_user.route('/users/<id>', methods=['GET'])
def get_user(id):
    try:
        user = User.get(User.id == id)
        userData = model_to_dict(user)
        return jsonify({'user': userData}), 201
    except Exception as identifier:
        return jsonify({'error': 'User not found {message}'.format(message=identifier.message)}), 404

# Update a specific user
@app_user.route('/users/<id>', methods=['PUT'])
def update_user(id):
    try:
        user = User.get(User.id == id)
        # Let's get the request
        params = request.get_json()
        if params.get('name', None) is not None:
            user.name = params.get('name')
        if params.get('password', None) is not None:
            user.password = hashlib.md5(params.get('password')).hexdigest()
        user.save()
        userData = model_to_dict(user)
        return jsonify({'user': userData}), 201
    except Exception as identifier:
        return jsonify({'error': 'Not found {message}'.format(message=identifier.message)}), 404

# Delete a specific user
@app_user.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.get(User.id == id)
        is_deleted = user.delete_instance()
        return str(is_deleted)
    except Exception as identifier:
        return jsonify({'error': 'Not found {message}.'.format(message=identifier.message)}), 404



# To delete
@app_user.route('/users/login', methods=['POST'])
def login():
    params = request.get_json()
    name = params.get('name')
    password = params.get('password')
    password_hashed = hashlib.md5(password).hexdigest()

    try:
        user = User.get(User.name == name)
        password = User.get(User.password == password_hashed)
        if user and password:
            token_gen = binascii.b2a_hex(os.urandom(16))
            data_user = model_to_dict(user)
            token = Token.create(token=token_gen, user_id=data_user['id'])
            token.save()
            data = model_to_dict(token)
            return jsonify({'response': 'User authentificated', 'token': data})
    except Exception as identifier:
        return jsonify({'response': 'User undefined'})
