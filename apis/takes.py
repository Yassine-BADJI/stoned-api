from flask import request
from flask_restplus import Namespace, fields, Resource

from apis.comun import token_required
from model import Takes, db

api = Namespace('takes', description='Takes path')

take_input = api.model('Take', {
    'date': fields.String(required=True, description='The date of the take'),
    'quantity': fields.String(required=True, description='The take quantity'),
    'unit': fields.String(required=True, description='The unit of the drug take'),
    'adress': fields.String(required=True, description='The adress of this take'),
    'latitude': fields.String(required=True, description='The latitude position'),
    'longitude': fields.String(required=True, description='The longitude position'),
    'drug_id': fields.Integer(required=True, description='The drug id of the take'),
})

token_parser = api.parser()
token_parser.add_argument('x-access-token', location='headers', required=True)


@api.route('/<id>')
class TakesByID(Resource):
    @api.doc('list_of_drugs_by_id')
    @api.expect(token_parser)
    @token_required
    def get(self, token_parser, id):
        take = Takes.query.filter_by(id=id).first()
        if not take:
            return {'message': 'No take found!'}
        take_data = {'id': take.id,
                     'date': take.date,
                     'quantity': take.quantity,
                     'unit': take.unit,
                     'adress': take.adress,
                     'latitude': take.latitude,
                     'longitude': take.longitude,
                     'drug_id': take.drug_id,
                     'user_id': take.user_id}
        return {'take': take_data}


@api.route('/user/<id>')
class TakeById(Resource):
    @api.doc('list_take_by_user_id')
    @api.expect(token_parser)
    @token_required
    def get(self, token_parser, id):
        takes = Takes.query.filter_by(user_id=id).all()
        if not takes:
            return {'message': 'No take found for this user!'}
        output = []
        for take in takes:
            take_data = {'id': take.id,
                         'date': take.date,
                         'quantity': take.quantity,
                         'unit': take.unit,
                         'adress': take.adress,
                         'latitude': take.latitude,
                         'longitude': take.longitude,
                         'drug_id': take.drug_id,
                         'user_id': take.user_id}
            output.append(take_data)
        return {'takes': output}

    @api.doc('add_new_take_for_user')
    @api.expect(token_parser, take_input)
    @token_required
    def post(self, token_parser, id):
        data = request.get_json()
        new_take = Takes(date=data['date'],
                         quantity=data['quantity'],
                         unit=data['unit'],
                         adress=data['adress'],
                         latitude=data['latitude'],
                         longitude=data['longitude'],
                         drug_id=data['drug_id'],
                         user_id=id)
        db.session.add(new_take)
        db.session.commit()
        return {'message': 'New take added!'}
