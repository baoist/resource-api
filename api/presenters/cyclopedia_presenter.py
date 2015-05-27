from marshmallow import Schema, fields, pprint
#from presenters.entries_presenter import EntriesPresenter


class CyclopediaPresenter(Schema):
    id = fields.Int()
    parent_cyclopedia_id = fields.Int()
    topic = fields.Str()
