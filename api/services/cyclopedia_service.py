from sqlalchemy import and_
from models.base import db
from models.cyclopedia import Cyclopedia
from models.user import User


class CyclopediaService(object):
    def init():
        pass


    def create(self, topic, user, parent_cyclopedias=None):
        parent_topic_id = self.get_immediate_parent(parent_cyclopedias)

        topics_at_level = self.topics_at_level(topic, user.id, None, parent_topic_id).count()
        if topics_at_level > 0:
            return False

        cyclopedia = Cyclopedia(topic, user.id, parent_topic_id)

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


    def get_immediate_parent(self, parent_topics=None):
        if not parent_topics:
            return None

        parents = [Cyclopedia.query.filter_by(topic = parent).first() for parent in parent_topics]
        nearest_topic_id = getattr(parents[-1], 'id', None)

        return nearest_topic_id
