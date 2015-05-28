from marshmallow import Schema, fields


class UserPresenter(Schema):
    username = fields.Str()
    auth_token = fields.Str()
    created_at = fields.Date()
