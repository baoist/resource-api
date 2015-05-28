from sqlalchemy import and_
from models.base import db
from models.cyclopedia import Cyclopedia


class CyclopediaService(object):
    def init():
        pass


    def create(self, topic, user, nodes=None):
        parent_node_id = self.get_parent_node(nodes)

        topics_at_level = self.topics_at_level(topic, user.id, None, parent_node_id).count()
        if topics_at_level > 0:
            return False

        cyclopedia = Cyclopedia(topic, user.id, parent_node_id)

        db.session.add(cyclopedia)
        db.session.commit()

        return cyclopedia


    def find(self, id):
        cyclopedia = Cyclopedia.query.filter_by(id = id).first()

        return cyclopedia


    def topics_at_level(self, topic, user_id, id=None, node_id=None):
        cyclopedias = db.session.query(Cyclopedia).filter(and_(
            Cyclopedia.topic == topic,
            Cyclopedia.user_id == user_id,
            Cyclopedia.id != id,
            Cyclopedia.parent_cyclopedia_id == node_id,
        ))

        return cyclopedias


    def get_parent_node(self, node_topics=None):
        if not node_topics:
            return None

        nodes = [Cyclopedia.query.filter_by(topic = node).first() for node in node_topics]
        nearest_topic_id = getattr(nodes[-1], 'id', None)

        return nearest_topic_id


    def get_root_cyclopedias(self, user_id):
        cyclopedias = db.session.query(Cyclopedia).filter(and_(
            Cyclopedia.user_id == user_id,
            Cyclopedia.node_cyclopedia_id == None,
        ))

        return cyclopedias
