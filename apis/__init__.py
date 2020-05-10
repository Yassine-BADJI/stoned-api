from flask_restplus import Api, fields

from .cats import api as ns_cats
from .hello import api as ns_hello
from .auth import api as ns_auth
from .drugs import api as ns_drugs
from .takes import api as ns_takes

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'x-access-token'
    }
}

api = Api(
    title='Stoned Api',
    version='0.8',
    description='Api for Stoned front-end',
    authorizations=authorizations
)

api.add_namespace(ns_cats)
api.add_namespace(ns_hello)
api.add_namespace(ns_auth)
api.add_namespace(ns_drugs)
api.add_namespace(ns_takes)


user_create_input = api.model('User', {
    'email': fields.String(required=True, description='The user email'),
    'password': fields.String(required=True, description='The user name'),
    'first_name': fields.String(required=True, description='The user first name'),
    'last_name': fields.String(required=True, description='The user last name'),
    'age': fields.String(required=True, description='The user age'),
})
