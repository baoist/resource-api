from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, types, ForeignKey
from models.mixins.dict_serializable_mixin import DictSerializableMixin
from base import db

import app

class Entry(db.Model, DictSerializableMixin):
    __tablename__ = 'entries'

    id = Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(255), index=True)
    title = db.Column(db.String(255))
    cyclopedia_id = db.Column(db.Integer, ForeignKey('cyclopedia.id'))
    image_url = db.Column(db.String(255))
    description = db.Column(db.Text())
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, topic, title, cyclopedia_id, image_url=None, description=None):
        self.topic = topic
        self.title = title
        self.cyclopedia_id = cyclopedia_id
        self.image_url = image_url
        self.description = description
