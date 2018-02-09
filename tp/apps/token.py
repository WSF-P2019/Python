import os,binascii
import hashlib
import time
from datetime import datetime
from datetime import timedelta
from flask import Blueprint, jsonify, request
from helpers.token_helper import token_helper
from models import Token
from models import User
from models import MobileCode
from playhouse.shortcuts import model_to_dict, dict_to_model

import nexmo
client = nexmo.Client(key='???"', secret='???"')

app_token = Blueprint('app_token', __name__)

# Get all our tokens
@app_token.route('/tokens', methods=['GET'])
def get_tokens():
    return jsonify({'tokens': list(Token.select().dicts()) }), 201

# Create our code for a specific user (with name and password given as login)
@app_token.route('/tokens/login/<id>', methods=['POST'])
def create_code(id):
  # Get the parameters
  params = request.get_json()
  paramsName = params.get('name')
  hashedParamsPassword = hashlib.md5(params.get('password')).hexdigest()
  # Check if there is already a token created
  try:
    tokenAlreadyCreated = Token.get(Token.user_id == id)
    return str('The ID given already match with a token')
  except:
    # Then check if there is an user with the ID given
    try:
      user = User.get(User.id == id)
      if user.name == paramsName and user.password == hashedParamsPassword:
        generatedMobileCode = binascii.b2a_hex(os.urandom(2))
        client.send_message({
          'from': 'Token - Python TP',
          'to': user.phone_number,
          'text': generatedMobileCode,
        })
        code = MobileCode.create(user_id=user.id, mobile_code=generatedMobileCode)
        code.save()
        codeData = model_to_dict(code)
        return jsonify({'response': 'Code well send for user:', 'code': codeData}), 201
      return str('Params given did not match to user ID')
    except Exception as identifier:
      return jsonify({'error': 'User not found {message}'.format(message=identifier.message)}), 404

# Create our token for a specific code (with code given in params)
@app_token.route('/tokens/validateCode', methods=['POST'])
def create_token():
  # Get the parameters
  params = request.get_json()
  paramsCode = params.get('code')
  try:
    code = MobileCode.get(MobileCode.mobile_code == paramsCode)
    if code.mobile_code == paramsCode:
      generatedToken = binascii.b2a_hex(os.urandom(16))
      currentTime = int(time.time())
      expirationDate = currentTime + 3600
      token = Token.create(token=generatedToken, user_id=code.user_id, created_at=currentTime, updated_at=currentTime, expiration_date=expirationDate)
      token.save()
      isDeleted = code.delete_instance()
      tokenData = model_to_dict(token)
      return jsonify({'response': 'Token well created for our user, and code well deleted', 'token': tokenData, 'code_deleted': isDeleted}), 201
    return str('Code given did not match to code generated')
  except Exception as identifier:
    return jsonify({'error': 'Code not found {message}'.format(message=identifier.message)}), 404

# Update expiration_date for a specific token
@app_token.route('/tokens/update/<id>', methods=['PUT'])
def update_token(id):
  # Get the parameters
  params = request.get_json()
  paramsName = params.get('name')
  hashedParamsPassword = hashlib.md5(params.get('password')).hexdigest()
 # Check if there is already a token created
  try:
    token = Token.get(Token.user_id == id)
    user = User.get(User.id == id)
    if user.name == paramsName and user.password == hashedParamsPassword:
      currentTime = int(time.time())
      token.updated_at = currentTime
      token.expiration_date = currentTime + 3600
      token.save()
      tokenData = model_to_dict(token)
      return jsonify({'token': tokenData}), 201
    else:
      return str('The ID / Password is not matching with the user_id given')
  except:
    return str('There is no token matching the user_id given')

# Delete a specific token
@app_token.route('/tokens/<id>', methods=['DELETE'])
def delete_token(id):
  try:
    token = Token.get(Token.id == id)
    is_deleted = token.delete_instance()
    return str(is_deleted)
  except Exception as identifier:
    return jsonify({'error': 'Not found {message}.'.format(message=identifier.message)}), 404
