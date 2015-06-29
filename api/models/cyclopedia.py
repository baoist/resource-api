from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey
from models.mixins.dict_serializable_mixin import DictSerializableMixin
from base import db

class Cyclopedia(db.Model, DictSerializableMixin):
    __tablename__ = 'cyclopedias'

    id = Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(255), index=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    parent_cyclopedia_id = db.Column(db.Integer, ForeignKey('cyclopedias.id'))
    cyclopedias = relationship("Cyclopedia")
    entries = relationship("Entry")
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, topic, user_id, parent_cyclopedia_id=None):
        self.topic = topic
        self.user_id = user_id
        self.parent_cyclopedia_id = parent_cyclopedia_id
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
