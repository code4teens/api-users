from marshmallow import fields, post_load, Schema

from models import User


class UserSchema(Schema):
    id = fields.Integer()
    password = fields.String(load_only=True)
    name = fields.String()
    discriminator = fields.String()
    display_name = fields.String()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
