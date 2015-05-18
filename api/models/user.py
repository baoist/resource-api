from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from collections import OrderedDict
from sqlalchemy import Column, types
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

import settings

db = SQLAlchemy()

class DictSerializableMixin(object):
    def _asdict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result

class User(db.Model, DictSerializableMixin):
    __tablename__ = 'users'

    id = Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    auth_token = db.Column(db.String(32), index=True)

    def __init__(self, name, username):
        self.name = name
        self.username = username
        self.auth_token = self.generate_auth_token

    def generate_auth_token(self, expiration=600):
        s = Serializer(config.SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(config.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user
