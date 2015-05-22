from functools import wraps
from flask.ext.httpauth import HTTPBasicAuth
from models.user import db, User

def authenticate(username_or_token, password=None):
    if password:
        return username_or_token
    else:
        return "no pw given"

def authenticate_with_password(username, password):
    user = "foo"

    return user
