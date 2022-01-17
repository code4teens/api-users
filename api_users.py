import bcrypt
from flask import Blueprint, request

from database import db_session
from models import User
from schemata import UserSchema

api_users = Blueprint('api_users', __name__)


@api_users.route('/users', methods=['POST'])
def create_user():
    keys = ['id', 'name', 'discriminator', 'display_name']

    if sorted([key for key in request.json]) == sorted(keys):
        id = request.json.get('id')
        name = request.json.get('name')
        discriminator = request.json.get('discriminator')
        existing_user_1 = User.query.filter_by(id=id).one_or_none()
        existing_user_2 = User.query.filter_by(name=name)\
            .filter_by(discriminator=discriminator)\
            .one_or_none()

        if existing_user_1 is not None or existing_user_2 is not None:
            data = {
                'title': 'Conflict',
                'status': 409
            }

            if existing_user_1 is not None:
                data['detail'] = f'User {id} already exists'
            else:
                data['detail'] = f'User {name}#{discriminator} already exists'

            return data, 409
        else:
            user_schema = UserSchema()

            try:
                user = user_schema.load(request.json)
            except Exception as _:
                data = {
                    'title': 'Bad Request',
                    'status': 400,
                    'detail': 'Some values failed validation'
                }

                return data, 400
            else:
                db_session.add(user)
                db_session.commit()
                data = {
                    'title': 'Created',
                    'status': 201,
                    'detail': f'User {id} created'
                }

                return data, 201
    else:
        data = {
            'title': 'Bad Request',
            'status': 400,
            'detail': 'Missing some keys or contains extra keys'
        }

        return data, 400


@api_users.route('/users/<int:id>/password', methods=['POST'])
def change_password(id):
    keys = ['old_password', 'new_password']

    if sorted([key for key in request.json]) == sorted(keys):
        user = User.query.filter_by(id=id).one_or_none()

        if user is not None:
            old_password = request.json.get('old_password')

            if bcrypt.checkpw(
                old_password.encode('utf-8'),
                user.password.encode('utf-8')
            ):
                new_password = request.json.get('new_password')

                try:
                    user.password = bcrypt.hashpw(
                        new_password.encode('utf-8'), bcrypt.gensalt()
                    )
                except Exception as _:
                    data = {
                        'title': 'Bad Request',
                        'status': 400,
                        'detail': 'Some values failed validation'
                    }

                    return data, 400
                else:
                    db_session.merge(user)
                    db_session.commit()
                    data = {
                        'title': 'OK',
                        'status': 200,
                        'detail': f'Updated password for user {id}'
                    }

                    return data, 200
            else:
                data = {
                    'title': 'Unauthorised',
                    'status': 401,
                    'detail': f'Wrong password for user {id}'
                }

                return data, 401
        else:
            data = {
                'title': 'Not Found',
                'status': 404,
                'detail': f'User {id} not found'
            }

            return data, 404
    else:
        data = {
            'title': 'Bad Request',
            'status': 400,
            'detail': 'Missing some keys or contains extra keys'
        }

        return data, 400
