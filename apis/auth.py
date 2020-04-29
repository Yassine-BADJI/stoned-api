import uuid
from functools import wraps

import jwt
from flask import request
from flask_restplus import Namespace, fields, Resource
from jwt import InvalidTokenError
from werkzeug.security import generate_password_hash

from model import User, db

api = Namespace('auth', description='User login authenfication')

user_model = api.model('User', {
    'id': fields.Integer(required=True, description='The id'),
    'name': fields.String(required=True, description='The user name'),
    'password': fields.String(required=True, description='The user name'),
    'admin': fields.Boolean(required=True, description='The admin status')
})

user_create_model = api.model('User', {
    'name': fields.String(required=True, description='The user name'),
    'password': fields.String(required=True, description='The user name'),
})


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return ({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, 'thisissecret')
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except InvalidTokenError:
            raise InvalidTokenError
            # return ({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)

    return decorated


@api.route('/users/')
@token_required
class Users(Resource):
    @api.doc('list_of_users')
    @api.marshal_list_with(user_model)
    def get(self, current_user):
        if not current_user.admin:
            return {'message': 'Vous n\' avez pas les permissions!'}
        users = User.query.all()
        output = []
        for user in users:
            user_data = {'public_id': user.public_id,
                         'name': user.name,
                         'password': user.password,
                         'admin': user.admin}
            output.append(user_data)
        return {'users': output}

    @api.doc('create_user')
    @api.marshal_list_with(user_create_model)
    def post(self, current_user):
        if not current_user.admin:
            return {'message': 'Vous n\' avez pas les permissions!'}
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'New user created!'}
