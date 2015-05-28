from sqlalchemy import and_
from models.base import db
from models.cyclopedia import Cyclopedia


class CyclopediaService(object):
    def init():
        pass


    def create(self, topic, user, nodes=None):
        '''
        Attempt to create a record

        Returns record if successful,
        otherwise returns False

        Receives a `topic` (required), `user` (required), `nodes` (optional)

        Record will be created as a child of the last node if passed,
        otherwise it will be at the root
        '''
        parent_node_id = self.get_parent_node_id(nodes)
        if nodes and not parent_node_id:
            return False

        topics_at_level = self.topics_at_level(topic, user.id, None, parent_node_id).count()
        if topics_at_level > 0:
            return False

        cyclopedia = Cyclopedia(topic, user.id, parent_node_id)

        db.session.add(cyclopedia)
        db.session.commit()

        return cyclopedia


    def find(self, id):
        '''
        Retrieve a single record given `id`
        '''
        cyclopedia = Cyclopedia.query.filter_by(id = id).first()

        return cyclopedia


    def topics_at_level(self, topic, user_id, id=None, node_id=None):
        '''
        Retrieves all records given
        topic, user_id, id (optional), node_id (optional)
        '''
        cyclopedias = db.session.query(Cyclopedia).filter(and_(
            Cyclopedia.topic == topic,
            Cyclopedia.user_id == user_id,
            Cyclopedia.id != id,
            Cyclopedia.parent_cyclopedia_id == node_id,
        ))

        return cyclopedias


    def get_parent_node_id(self, node_topics=None):
        '''
        Retreive the id of the last record in a path
        given a path of `topics`
        '''
        nearest_topic = self.get_parent_node(node_topics)

        return getattr(nearest_topic, 'id', None)

    def get_parent_node(self, node_topics=None):
        '''
        Retreive all node records in a path
        '''
        if not node_topics:
            return None

        nodes = []
        previous = None
        for iter, topic in enumerate(node_topics):
            node = Cyclopedia.query.filter(and_(
                Cyclopedia.topic == topic,
                Cyclopedia.parent_cyclopedia_id == getattr(previous, 'id', None)
            )).first()

            nodes.append(node)
            previous = node

        if not all(nodes):
            return None

        return nodes[-1]


    def get_root_cyclopedias(self, user_id):
        '''
        Retreive all root nodes
        '''
        cyclopedias = db.session.query(Cyclopedia).filter(and_(
            Cyclopedia.user_id == user_id,
            Cyclopedia.node_cyclopedia_id == None,
        ))

        return cyclopedias
