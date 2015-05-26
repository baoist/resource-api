from functools import wraps
from flask import (g, request, Response, redirect,
                  url_for, Flask, jsonify)
from flask.ext.httpauth import HTTPBasicAuth
from models.base import db
from models.user import User
from models.cyclopedia import Cyclopedia
from authentication.verification import Authenticator

import config

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.auth = HTTPBasicAuth()
db.init_app(app)

def require_apikey(fn):
    def _wrap(*args, **kwargs):
        auth = request.authorization
        authenticator = Authenticator(auth.username)
        user = authenticator.authenticate()

        if not auth.username or not user:
            return Response(response='401 Unauthorized.',
                        status=401,
                        mimetype="application/json")

        g.user = user
        return fn(*args, **kwargs)
    return _wrap

@app.route("/api/users/create", methods=["POST"])
def create_user():
    auth = request.authorization
    user = User(auth.username, auth.password)

    db.session.add(user)
    db.session.commit()

    return "test"

@app.route("/api/log-in", methods=["POST"])
def login():
    auth = request.authorization

    authenticator = Authenticator(auth.username, auth.password)
    user = authenticator.authenticate()

    if not user:
        return Response(response='401 Unauthorized.',
                        status=401,
                        mimetype="application/json")

    g.user = user
    return jsonify(user = user._asdict())

@app.route("/")
def hello():
    return "test"

@app.route("/foo")
@require_apikey
def foo():
    return "Goodbye, %s!" % g.user.password


@app.route("/bar")
def bar():
    return "Goodbye World!"

@app.route("/wib")
def wib():
    return "Goodbye World!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
