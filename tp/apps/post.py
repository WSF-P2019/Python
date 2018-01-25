from flask import Blueprint, jsonify
from helpers.post_helper import post_helper
from models import Post

app_post = Blueprint('app_post', __name__)

@app_post.route('/posts', methods=['GET', 'POST'])
def app():
  post = Post.create(title='lol', description='la bonne description')
  post.save()
  return jsonify({'data': list(Post.select().dicts()) }), 201
