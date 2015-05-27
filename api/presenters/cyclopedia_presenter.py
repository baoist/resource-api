from marshmallow import Schema, fields, pprint
#from presenters.entries_presenter import EntriesPresenter


class CyclopediaPresenter(Schema):
    id = fields.Int()
    parent_cyclopedia_id = fields.Int(default=None)
    topic = fields.Str()
    cyclopedias = fields.Nested('self', many=True, default=None)
