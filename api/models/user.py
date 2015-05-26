from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, types
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as URLSafeSerializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context as pwd_context
from models.mixins.dict_serializable_mixin import DictSerializableMixin
from base import db

import app

class User(db.Model, DictSerializableMixin):
    __tablename__ = 'users'

    id = Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True)
    password = db.Column(db.String(255))
    auth_token = db.Column(db.String(255), index=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, username, password):
        self.username = username
        self.password = self.hash_password(password)
        self.auth_token = self.generate_auth_token()
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def generate_auth_token(self, expiration=600):
        s = URLSafeSerializer(app.config.Config.SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id})

    def get_id(self):
        return unicode(self.id)

    def hash_password(self, password):
        return pwd_context.encrypt(password)

    def verify_auth_token(self, token):
        s = URLSafeSerializer(app.config.Config.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data['id'])
        return user

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)
