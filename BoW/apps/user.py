#-*- coding: utf-8 -*-
import hashlib
from flask import Blueprint, jsonify, request
from helpers.user_helper import user_helper
from helpers.token_helper import token_helper
from models import User
from models import Token
from playhouse.shortcuts import model_to_dict, dict_to_model

app_user = Blueprint('app_user', __name__)

@app_user.route('/users', methods=['POST'])
def create_user():
    # Récupération de la requête
    params = request.get_json()
    name = params.get('name')
    password = params.get('password')
    password_hashed = hashlib.md5(password).hexdigest()

    # Création du user
    user = User.create(name=name, password=password_hashed)
    user.save()

    # Convertion du user en dictionnaire
    data = model_to_dict(user)

    # Envoi de l'information en format json
    return jsonify({'user': data}), 201

@app_user.route('/users', methods=['GET'])
def get_all_users():
    return jsonify({'users': list(User.select().dicts()) }), 201

@app_user.route('/user/<id>', methods=['GET'])
def get_user(id):
    try:
        user = User.get(User.id == id)
        data = model_to_dict(user)
        return jsonify({'user': data}), 201
    except Exception as identifier:
        return jsonify({'error': 'Not found {message}'.format(message=identifier.message)}), 404

@app_user.route('/user/<id>', methods=['PUT'])
def update_user(id):
    try:
        user = User.get(User.id == id)
        params = request.get_json()
        if params.get('name', None) is not None:
            user.name = params.get('name')
        if params.get('password', None) is not None:
            user.password = hashlib.md5(params.get('password')).hexdigest()
        user.save()
        data = model_to_dict(user)
        return jsonify({'user': data}), 201
    except Exception as identifier:
        return jsonify({'error': 'Not found {message}'.format(message=identifier.message)}), 404

@app_user.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.get(User.id == id)
        is_deleted = user.delete_instance()
        return str(is_deleted)
    except Exception as identifier:
        return jsonify({'error': 'Not found {message}'.format(message=identifier.message)}), 404

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
            token_gen = hashlib.md5('test').hexdigest()
            print token_gen
            uid = User.get(User.id)
            token = Token.create(user_id=uid, token=token_gen)
            token.save()
            data = model_to_dict(token)
            return jsonify({'response': 'User authentificated', 'token': data})
    except Exception as identifier:
        return jsonify({'response': 'User undefined'})
        