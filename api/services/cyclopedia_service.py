from sqlalchemy import and_
from models.base import db
from models.cyclopedia import Cyclopedia
from models.user import User


class CyclopediaService():
    def init():
        pass


    def create(self, topic, user, parent_cyclopedia_path=None):
        topics_at_level = self.topics_at_level(topic, user.id).count()
        if topics_at_level > 0:
            return False

        cyclopedia = Cyclopedia(topic, user.id)

        db.session.add(cyclopedia)
        db.session.commit()

        return cyclopedia

    def topics_at_level(self, topic, user_id, id=None, parent_cyclopedia_id=None):
        cyclopedias = db.session.query(Cyclopedia).filter(and_(
            Cyclopedia.topic == topic,
            Cyclopedia.user_id == user_id,
            Cyclopedia.id != id,
            Cyclopedia.parent_cyclopedia_id == parent_cyclopedia_id,
        ))

        return cyclopedias
