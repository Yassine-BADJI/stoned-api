from flask_restplus import Namespace, Resource

api = Namespace('hello', description='Hello world display')

HELLO = {'hello': 'world'}


@api.route('/')
class HelloWorld(Resource):
    @api.doc('hello_world')
    def get(self):
        return HELLO
