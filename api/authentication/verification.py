from functools import wraps
from flask.ext.httpauth import HTTPBasicAuth
from models.user import db, User

class Authenticator():
    def __init__(self, username_or_token, password=None):
        self.username = self.token = username_or_token
        self.password = password

        if self.password:
            self.method = "authenticate_with_password"
        else:
            self.method = "authenticate_with_token"

    def authenticate(self):
        return getattr(self, self.method)()

    def authenticate_with_password(self):
        user = User.query.filter_by(username = self.username).first()
        if not user or not user.verify_password(self.password):
            return False
        return user

    def authenticate_with_token(self):
        user = User.query.filter_by(auth_token = self.token).first()
        if not user:
            return False
        return user
