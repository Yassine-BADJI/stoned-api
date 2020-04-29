import datetime
from functools import wraps

import jwt
from flask import request, make_response
from flask_restplus import Namespace, fields, Resource
from jwt import InvalidTokenError
from werkzeug.security import generate_password_hash, check_password_hash

from model import User, db
from config import key

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

token_parser = api.parser()
token_parser.add_argument('x-access-token', location='headers', required=True)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return ({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, key)
            current_user = User.query.filter_by(id=data['id']).first()
        except InvalidTokenError:
            return ({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated


@api.route('/users/login')
class UsersLogin(Resource):
    @api.doc('login_user')
    def get(self):
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
        user = User.query.filter_by(name=auth.username).first()
        if not user:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
        if check_password_hash(user.password, auth.password):
            token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
                               key)
            return {'token': token.decode('UTF-8')}
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


@api.route('/users/')
class Users(Resource):
    @api.doc('list_of_users')
    @api.expect(token_parser)
    @token_required
    def get(self, token_parser):
        # if not token_parser.current_user.admin:
        #     return {'message': 'Vous n\' avez pas les permissions!'}
        users = User.query.all()
        output = []
        for user in users:
            user_data = {'name': user.name,
                         'password': user.password,
                         'admin': user.admin}
            output.append(user_data)
        return {'users': output}

    @api.doc('create_user')
    @api.expect(user_create_model)
    def post(self):
        # if not current_user.admin:
        #     return {'message': 'Vous n\' avez pas les permissions!'}
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = User(name=data['name'], password=hashed_password, admin=False)
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'New user created!'}


@api.route('/users/<id>')
class UsersID(Resource):
    @api.doc('promote_user')
    @api.expect(token_parser)
    @token_required
    def put(self, token_parser, id):
        # if not current_user.admin:
        #     return {'message': 'Vous n\' avez pas les permissions!'}
        user = User.query.filter_by(id=id).first()
        if not user:
            return {'message': 'No user found!'}
        user.admin = True
        db.session.commit()
        return {'message': 'The user has been promoted!'}

    @api.doc('delete_user')
    @api.expect(token_parser)
    @token_required
    def delete(self, token_parser, id):
        # if not current_user.admin:
        #     return {'message': 'Vous n\' avez pas les permissions!'}
        user = User.query.filter_by(id=id).first()
        if not user:
            return {'message': 'No user found!'}
        db.session.delete(user)
        db.session.commit()
        return {'message': 'The user has been deleted!'}
