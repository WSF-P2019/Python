from flask import Blueprint, jsonify, request
from helpers.post_helper import post_helper
from models import Post
from playhouse.shortcuts import model_to_dict, dict_to_model

app_post = Blueprint('app_post', __name__)

# Create article
@app_post.route('/posts', methods=['POST'])
def create_post():
  params = request.get_json() # dict
  title = params.get('title')
  description = params.get('description')

  post = Post.create(title=title, description=description)
  post.save()

  # Convert our model (object) to dictionnary
  data = model_to_dict(post)
  # Jsonify work only with dict, we've to convert everything
  return jsonify({'data': data}), 201

# Create article
@app_post.route('/post/<id>', methods=['GET'])
def get_post(id):
  post = Post.get(Post.id == id)
  # We convert once again
  data = model_to_dict(post)

  # We send the information to the browser
  return jsonify({'data': data}), 201
