import bcrypt
from flask import Blueprint, request

from database import db_session
from models import User

api_users = Blueprint('api_users', __name__)


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
