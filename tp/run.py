from flask import Flask
from apps.hello import app_hello
from apps.post import app_post

app = Flask(__name__)
app.register_blueprint(app_hello)
app.register_blueprint(app_post)


if __name__ == "__main__":
    app.run(debug=True, port=3000)
