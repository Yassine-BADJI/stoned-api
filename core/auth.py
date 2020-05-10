import datetime

import jwt
from flask import request, make_response
from sendgrid.helpers.mail import Mail
from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from config import key
from external_ressource.sendgrid import send_mail
from model import User, db


def check_is_admin(user):
    if not user.admin:
        raise BadRequest('You are not allowed to use this method!')


def check_is_exist(user):
    if not user:
        raise BadRequest('No user found!')


def add_new_user(data):
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(email=data['email'],
                    password=hashed_password,
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    age=data['age'])
    db.session.add(new_user)
    db.session.commit()
    send_welcome(new_user.email)


def get_a_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    check_is_exist(user)
    return user


def get_all_users():
    users = User.query.all()
    return users


def send_welcome(user_email):
    message = Mail(
        from_email='kemisse@hotmail.com',
        to_emails=user_email,
        subject='Bienvenue sur stoned',
        html_content='<strong>Nous te sommes ravi de te compter parmis nos nouveaux membres</strong>')
    send_mail(message)


def user_login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    user = User.query.filter_by(email=auth.username).first()
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
                           key)
        user_token = {'token': token.decode('UTF-8'),
                      'user_id': user.id}
        return {'token': user_token}
    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
