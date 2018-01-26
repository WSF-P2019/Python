from flask import Blueprint, jsonify, request
from helpers.post_helper import post_helper
from models import Post

app_post = Blueprint('app_post', __name__)

# Create article
@app_post.route('/posts', methods=['POST'])
def create_post():
  params = request.get_json() # dict
  title = params.get('title')
  description = params.get('description')
  print title, description

  # post = Post.create(title='lol', description='la bonne description')
  # post.save()

  # return jsonify({'data': list(Post.select().dicts()) }), 201
  return 'test'
