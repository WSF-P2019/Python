from flask import Flask
from apps.hello import app_hello

app = Flask(__name__)
app.register_blueprint(app_hello)


if __name__ == "__main__":
    app.run(debug=True, port=3000)
