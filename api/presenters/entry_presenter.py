from marshmallow import Schema, fields


class EntryPresenter(Schema):
    id = fields.Int()
    cyclopedia_id = fields.Int(default=None)
    term = fields.Str()
    title = fields.Str()
    image_url = fields.Str()
    description = fields.Str()
