from functools import wraps
from flask import g, request, redirect, url_for, Flask
from flask.ext.httpauth import HTTPBasicAuth
from models.user import db, User

app = Flask(__name__)
auth = HTTPBasicAuth()
db.init_app(app)

def require_apikey(f):
    @wraps(f)
    def require_key(*args, **kwargs):
        return f(*args, **kwargs)
    return require_key

@auth.verify_password
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

@app.route("/api/log-in", methods=["POST"])
def login():
    auth = request.authorization
    verified = verify_password(auth.username, auth.password)

    return "foo"

@app.route("/")
def hello():
    return "Hello World!"

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
