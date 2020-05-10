from flask_restplus import Api

from .auth import api as ns_auth
from .drugs import api as ns_drugs
from .hello import api as ns_hello
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

api.add_namespace(ns_hello)
api.add_namespace(ns_auth)
api.add_namespace(ns_drugs)
api.add_namespace(ns_takes)
