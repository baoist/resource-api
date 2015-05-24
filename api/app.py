from functools import wraps
from flask import (g, request, redirect,
                  url_for, Flask, jsonify)
from flask.ext.httpauth import HTTPBasicAuth
from models.user import db, User
from authentication.verification import Authenticator

import config

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.auth = HTTPBasicAuth()
db.init_app(app)

def require_apikey(f):
    @wraps(f)
    def require_key(*args, **kwargs):
        return f(*args, **kwargs)
    return require_key

@app.route("/api/users/create", methods=["POST"])
def create_user():
    auth = request.authorization
    user = User(auth.username, auth.password)

    db.session.add(user)
    db.session.commit()

    return "test"

@app.route("/api/log-in", methods=["POST"])
@app.auth.verify_password
def login():
    auth = request.authorization

    authenticator = Authenticator(auth.username, auth.password)
    user = authenticator.authenticate()

    if not user:
        return False

    g.user = user
    return jsonify(user = user._asdict())
    #return "Hello, %s!" % user.authentication_token

@app.route("/")
def hello():
    return "test"

@app.route("/foo")
def foo():
    return "Goodbye World!"

@app.route("/bar")
def bar():
    return "Goodbye World!"

@app.route("/wib")
def wib():
    return "Goodbye World!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
