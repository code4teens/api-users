from marshmallow import fields, post_load, Schema

from models import User


class UserSchema(Schema):
    id = fields.Integer()
    password = fields.String(load_only=True)
    name = fields.String()
    discriminator = fields.String()
    display_name = fields.String()
    is_admin = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    last_updated = fields.DateTime(dump_only=True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
