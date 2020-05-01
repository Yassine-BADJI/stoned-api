import datetime

import jwt
from flask import request, make_response
from flask_restplus import Namespace, fields, Resource
from werkzeug.security import generate_password_hash, check_password_hash

from apis.comun import token_required
from config import key
from model import User, db

api = Namespace('auth', description='User login authenfication')

user_create_input = api.model('User', {
    'email': fields.String(required=True, description='The user email'),
    'password': fields.String(required=True, description='The user name'),
    'first_name': fields.String(required=True, description='The user first name'),
    'last_name': fields.String(required=True, description='The user last name'),
    'age': fields.String(required=True, description='The user age'),
})

token_parser = api.parser()
token_parser.add_argument('x-access-token', location='headers', required=True)


@api.route('/users/login')
class UsersLogin(Resource):
    @api.doc('login_user')
    def get(self):
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
        user = User.query.filter_by(email=auth.username).first()
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
        #     return {'message': 'You are not allowed to use this method!'}
        users = User.query.all()
        output = []
        for user in users:
            user_data = {'first_name': user.first_name,
                         'last_name': user.last_name,
                         'email': user.email,
                         'age': user.age,
                         'admin': user.admin}
            output.append(user_data)
        return {'users': output}

    @api.doc('create_user')
    @api.expect(user_create_input)
    def post(self):
        # if not token_parser.current_user.admin:
        #     return {'message': 'You are not allowed to use this method!'}
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = User(email=data['email'],
                        password=hashed_password,
                        first_name=data['first_name'],
                        last_name=data['last_name'],
                        age=data['age'])
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'New user created!'}


@api.route('/users/<id>')
class UsersID(Resource):
    @api.doc('promote_user')
    @api.expect(token_parser)
    @token_required
    def put(self, token_parser, id):
        # if not token_parser.current_user.admin:
        #     return {'message': 'You are not allowed to use this method!'}
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
        # if not token_parser.current_user.admin:
        #     return {'message': 'You are not allowed to use this method!'}
        user = User.query.filter_by(id=id).first()
        if not user:
            return {'message': 'No user found!'}
        db.session.delete(user)
        db.session.commit()
        return {'message': 'The user has been deleted!'}
