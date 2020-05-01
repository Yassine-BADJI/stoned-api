from functools import wraps

import jwt
from flask import request
from jwt import InvalidTokenError

from config import key
from model import User


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
