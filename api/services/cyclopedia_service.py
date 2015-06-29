from sqlalchemy import and_
from models.base import db
from models.cyclopedia import Cyclopedia


class CyclopediaService(object):
    def init():
        pass

    def create(self, topic, user, nodes=None):
        """
        Attempt to create a record

        Returns record if successful,
        otherwise returns False

        Record will be created as a child of the last node if passed,
        otherwise it will be at the root
        """
        if nodes:
            # new record should be created as a
            # child of the last node in nodes
            parent_node = self.get_parent_node_by_topic_path(user, nodes)

            if not parent_node:
                return False

        else:
            # default to root node
            parent_node = self.get_root_node(user)

            if not parent_node:
                # create root node if not yet existing
                parent_node = self.create_root_node(user)

        parent_node_id = getattr(parent_node, 'id', None)
        if not parent_node_id:
            return False

        topics_at_level = self.topics_at_level(topic, user.id, None, parent_node_id).scalar()
        if topics_at_level:
            return False

        cyclopedia = Cyclopedia(topic, user.id, parent_node_id)

        db.session.add(cyclopedia)
        db.session.commit()

        return cyclopedia

    def get_root_node(self, user):
        node = Cyclopedia.query.filter(and_(
            Cyclopedia.user_id == user.id,
            Cyclopedia.parent_cyclopedia_id.is_(None),
        )).first()

        return node

    def create_root_node(self, user):
        node = Cyclopedia("Root Cyclopedia", user.id, None)

        db.session.add(node)
        db.session.commit()

        return node

    def find(self, id):
        """
        Retrieve a single record given `id`
        """
        cyclopedia = Cyclopedia.query.filter(Cyclopedia.id == id).first()

        return cyclopedia

    def topics_at_level(self, topic, user_id, id=None, node_id=None):
        """
        Retrieves all records given
        topic, user_id, id (optional), node_id (optional)
        """
        cyclopedias = db.session.query(Cyclopedia).filter(and_(
            Cyclopedia.topic == topic,
            Cyclopedia.user_id == user_id,
            Cyclopedia.id != id,
            Cyclopedia.parent_cyclopedia_id == node_id,
        ))

        return cyclopedias

    def get_parent_node_by_topic_path(self, user, node_topics=None):
        """
        Retreive all node records in a path
        """
        if not node_topics:
            return None

        nodes = []
        previous = self.get_root_node(user)
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

    def get_root_cyclopedia(self, user_id):
        """
        Retreive all root nodes
        """
        cyclopedias = db.session.query(Cyclopedia).filter(and_(
            Cyclopedia.user_id == user_id,
            Cyclopedia.parent_cyclopedia_id.is_(None),
        )).first()

        return cyclopedias
