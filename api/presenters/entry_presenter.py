from marshmallow import Schema, fields


class EntryPresenter(Schema):
    id = fields.Int()
    cyclopedia_id = fields.Int(default=None)
    topic = fields.Str()
    image_url = fields.Str()
    description = fields.Str()
