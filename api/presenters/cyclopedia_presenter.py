from marshmallow import Schema, fields
from presenters.entry_presenter import EntryPresenter


class CyclopediaPresenter(Schema):
    id = fields.Int()
    parent_cyclopedia_id = fields.Int(default=None)
    topic = fields.Str()
    cyclopedias = fields.Nested('self', many=True, default=None)
    entries = fields.Nested(EntryPresenter, many=True, default=None)
