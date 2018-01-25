from flask import Blueprint, jsonify
from helpers.hello_helper import hello_helper
from models import User

app_hello = Blueprint('app_hello', __name__)

@app_hello.route('/', methods=['GET', 'POST'])
def app():

    charlie = User.create(email='charlie', password='test')
    charlie.save()

    # return jsonify({'data': 'hello ' + hello_helper()}), 201
    users = User.select()
    for user in User.select().dicts():
        print user['email']
    return jsonify({'data': User.select()}), 201
