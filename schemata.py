from marshmallow import fields, post_load, Schema

from models import Enrolment, User


class UserSchema(Schema):
    id = fields.Integer()
    password = fields.String(load_only=True)  # TODO: phase-out
    name = fields.String()
    discriminator = fields.String()
    display_name = fields.String()
    is_admin = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    last_updated = fields.DateTime(dump_only=True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


class BasicUserSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    discriminator = fields.String()
    display_name = fields.String()


class BasicCohortSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    nickname = fields.String()
    duration = fields.Integer()
    start_date = fields.Date()


class EnrolmentSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(load_only=True)
    cohort_id = fields.Integer(load_only=True)

    user = fields.Nested('BasicUserSchema', dump_only=True)
    cohort = fields.Nested('BasicCohortSchema', dump_only=True)

    @post_load
    def make_enrolment(self, data, **kwargs):
        return Enrolment(**data)
