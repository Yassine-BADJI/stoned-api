from flask_restplus import Api

from .cats import api as ns_cats
from .hello import api as ns_hello
from .auth import api as ns_auth
from .drugs import api as ns_drugs
from .takes import api as ns_takes


api = Api(
    title='Stoned Api',
    version='0.1',
    description='Fucking Api for prevention',
    # All API metadatas
)

api.add_namespace(ns_cats)
api.add_namespace(ns_hello)
api.add_namespace(ns_auth)
api.add_namespace(ns_drugs)
api.add_namespace(ns_takes)
