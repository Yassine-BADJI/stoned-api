from flask import request
from flask_restplus import Namespace, Resource, fields

from apis.comun import token_required
from core.auth import add_new_user, check_is_admin, get_a_user, get_all_users, user_login
from model import db

api = Namespace('users', description='User login authenfication')

user_create_input = api.model('User', {
    'email': fields.String(required=True, description='The user email'),
    'password': fields.String(required=True, description='The user name'),
    'first_name': fields.String(required=True, description='The user first name'),
    'last_name': fields.String(required=True, description='The user last name'),
    'age': fields.String(required=True, description='The user age'),
})


@api.route('/login')
class UsersLogin(Resource):
    @api.doc('login_user')
    def get(self):
        return user_login()


@api.route('/')
class Users(Resource):
    @api.doc(security='apikey')
    @token_required
    def get(self, current_user):
        check_is_admin(self)
        users = get_all_users()
        output = []
        for user in users:
            user_data = {'user_id': user.id,
                         'first_name': user.first_name,
                         'last_name': user.last_name,
                         'email': user.email,
                         'age': user.age,
                         'admin': user.admin}
            output.append(user_data)
        return {'users': output}

    @api.doc('create_user')
    @api.expect(user_create_input)
    def post(self):
        data = request.get_json()
        add_new_user(data)
        return {'message': 'New user created!'}


@api.route('/<id>')
class UsersID(Resource):
    @api.doc(security='apikey')
    @token_required
    def get(self, current_user, id):
        check_is_admin(self)
        user = get_a_user(id)
        user_data = {'user_id': user.id,
                     'first_name': user.first_name,
                     'last_name': user.last_name,
                     'email': user.email,
                     'age': user.age,
                     'admin': user.admin}
        return {'user': user_data}

    @api.doc(security='apikey')
    @token_required
    def put(self, current_user, id):
        check_is_admin(self)
        user = get_a_user(id)
        user.admin = True
        db.session.commit()
        return {'message': 'The user has been promoted!'}

    @api.doc(security='apikey')
    @token_required
    def delete(self, current_user, id):
        check_is_admin(self)
        user = get_a_user(id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'The user has been deleted!'}
