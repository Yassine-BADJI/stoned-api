from flask import request
from flask_restplus import Namespace, fields, Resource
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import exc

from apis.comun import token_required
from core.auth import check_current_user
from core.drugs import get_drug_by
from core.takes import get_takes_by, get_all_takes_by
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


@api.route('/<int:id>')
class TakesByID(Resource):
    @api.doc(security='apikey')
    @token_required
    def get(self, current_user, id):
        take = get_takes_by('id', id)
        drug = get_drug_by('id', take.drug_id)
        take_data = {'id': take.id,
                     'date': take.date,
                     'quantity': take.quantity,
                     'unit': take.unit,
                     'adress': take.adress,
                     'latitude': take.latitude,
                     'longitude': take.longitude,
                     'drug_id': take.drug_id,
                     'drug_name': drug.name,
                     'user_id': take.user_id}
        return {'take': take_data}


@api.route('/user/<int:id>')
class TakeById(Resource):
    @api.doc(security='apikey')
    @token_required
    def get(self, current_user, id):
        check_current_user(self, id)
        takes = get_all_takes_by('user_id', id)
        output = []
        for take in takes:
            drug = get_drug_by('id', take.drug_id)
            take_data = {'id': take.id,
                         'date': take.date,
                         'quantity': take.quantity,
                         'unit': take.unit,
                         'adress': take.adress,
                         'latitude': take.latitude,
                         'longitude': take.longitude,
                         'drug_id': take.drug_id,
                         'drug_name': drug.name,
                         'user_id': take.user_id}
            output.append(take_data)
        return {'takes': output}

    @api.expect(take_input)
    @api.doc(security='apikey')
    @token_required
    def post(self, current_user, id):
        check_current_user(self, id)
        data = request.get_json()
        new_take = Takes(date=data['date'],
                         quantity=data['quantity'],
                         unit=data['unit'],
                         adress=data['adress'],
                         latitude=data['latitude'],
                         longitude=data['longitude'],
                         drug_id=data['drug_id'],
                         user_id=id)
        try:
            db.session.add(new_take)
            db.session.commit()
            return {'message': 'New take added!'}
        except IntegrityError as e:
            db.session.rollback()
            return{'error': e.__cause__}
