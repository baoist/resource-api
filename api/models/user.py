from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import relationship
from collections import OrderedDict
from sqlalchemy import Column, types
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

import config

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
    password = db.Column(db.String(50))
    auth_token = db.Column(db.String(32), index=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.auth_token = self.generate_auth_token()
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def generate_auth_token(self, expiration=600):
        #s = Serializer(config.SECRET_KEY, expires_in=expiration)
        #return s.dumps({'id': self.id})
        return "foo"

    def get_id(self):
        return unicode(self.id)

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
