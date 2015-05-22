from functools import wraps
from flask import g, request, redirect, url_for, Flask
from flask.ext.httpauth import HTTPBasicAuth
from models.user import db, User

from authentication.verification import authenticate
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

def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

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

    user = authenticate(auth.username, auth.password)

    return "Hello, %s!" % user

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
