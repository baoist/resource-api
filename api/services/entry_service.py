from sqlalchemy import and_
from models.base import db
from models.entry import Entry
from services.cyclopedia_service import CyclopediaService


class EntryService(object):
    cyclopedia_service = CyclopediaService()

    def init():
        pass


    def create(self, term, user, title, image_url=None, description=None, nodes=None):
        """
        Attempt to create a record

        Returns record if successful,
        otherwise returns False

        Record will be created as a child of the last node if passed,
        otherwise it will be at the root
        """
        if not nodes:
            parent_node = self.cyclopedia_service.get_root_node(user)
        else:
            parent_node = self.cyclopedia_service.get_parent_node_by_topic_path(user, nodes)
            if nodes and not parent_node:
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
        entries = db.session.query(Entry).filter(and_(
            Entry.user_id == user_id,
            Entry.cyclopedia_id == None,
        )).all()

        return entries
