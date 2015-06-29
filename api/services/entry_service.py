from sqlalchemy import and_
from models.base import db
from models.entry import Entry
from services.cyclopedia_service import CyclopediaService


class EntryService(object):
    cyclopedia_service = CyclopediaService()

    def init():
        pass

    def create(self, term, user, title,
               image_url=None, description=None, nodes=None):
        """
        Attempt to create a record

        Returns record if successful,
        otherwise returns False

        Record will be created as a child of the last node if passed,
        otherwise it will be at the root node
        """
        if not nodes:
            parent_node = self.cyclopedia_service.get_root_node(user)
        else:
            parent_node = self.cyclopedia_service.get_parent_node_by_topic_path(user, nodes)
            if not parent_node:
                return False

        parent_node_id = getattr(parent_node, 'id', None)

        terms_at_level = self.terms_at_level(term, user.id, None, parent_node_id).count()
        if terms_at_level > 0:
            return False

        entry = Entry(term, title, user.id, parent_node_id, image_url, description)

        db.session.add(entry)
        db.session.commit()

        return entry

    def terms_at_level(self, term, user_id, id=None, node_id=None):
        """
        Retrieves all records at level given params
        """
        entries = db.session.query(Entry).filter(and_(
            Entry.term == term,
            Entry.user_id == user_id,
            Entry.id != id,
            Entry.cyclopedia_id == node_id,
        ))

        return entries

    def get_root_entries(self, user_id):
        """
        Retreive all root nodes
        """
        # TODO: set Entry.cyclopedia_id to Cyclopedia root node id
        entries = db.session.query(Entry).filter(and_(
            Entry.user_id == user_id,
            Entry.cyclopedia_id.is_(None),
        )).all()

        return entries

    def find(self, user_id, id):
        """
        Retrieve a single record given `user_id` and `id`
        """
        entry = db.session.query(Entry).filter(and_(
            Entry.user_id == user_id,
            Entry.id == id,
        )).first()

        return entry

    def destroy(self, entry):
        """
        Destroy a single record given `entry`
        """
        db.session.delete(entry)
        db.session.commit()

        return True
