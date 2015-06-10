from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, types, ForeignKey
from models.mixins.dict_serializable_mixin import DictSerializableMixin
from base import db

import app

# TODO: Add URL

class Entry(db.Model, DictSerializableMixin):
    __tablename__ = 'entries'

    id = Column(db.Integer, primary_key=True)
    term = db.Column(db.String(255), index=True)
    title = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    description = db.Column(db.Text())
    cyclopedia_id = db.Column(db.Integer, ForeignKey('cyclopedias.id'))
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, term, title, user_id, cyclopedia_id=None, image_url=None, description=None):
        self.term = term
        self.title = title
        self.image_url = image_url
        self.description = description
        self.cyclopedia_id = cyclopedia_id
        self.user_id = user_id
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
