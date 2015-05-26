from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, types, ForeignKey
from models.mixins.dict_serializable_mixin import DictSerializableMixin
from base import db

import app

class Cyclopedia(db.Model, DictSerializableMixin):
    __tablename__ = 'cyclopedias'

    id = Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(255), index=True)
    title = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    description = db.Column(db.Text())
    parent_cyclopedia_id = db.Column(db.Integer, ForeignKey('cyclopedia.id'))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, topic, title, image_url=None, description=None, parent_cyclopedia_id=None):
        self.topic = topic
        self.title = title
        self.image_url = image_url
        self.description = description
        self.parent_cyclopedia_id = parent_cyclopedia_id
