from flask_restplus import Namespace, Resource

from apis.comun import token_required
from model import Drugs, Types

api = Namespace('drugs', description='Drugs path')

token_parser = api.parser()
token_parser.add_argument('x-access-token', location='headers', required=True)


@api.route('/')
class DrugsAll(Resource):
    @api.doc('list_all_drugs')
    @api.expect(token_parser)
    @token_required
    def get(self, token_parser):
        drugs = Drugs.query.all()
        output = []
        for drug in drugs:
            drug_data = {'id': drug.id,
                         'name': drug.name,
                         'summary': drug.summary,
                         'legal_status': drug.legal_status,
                         'drug_testing': drug.drug_testing,
                         'way_consuming': drug.way_consuming,
                         'desired_effect': drug.desired_effect,
                         'secondary_effect': drug.secondary_effect,
                         'risks_complications': drug.risks_complications,
                         'addiction': drug.addiction,
                         'risk_reduction_tips': drug.risk_reduction_tips,
                         'img': drug.img,
                         'type_id': drug.type_id}
            output.append(drug_data)
        return {'drug': output}


@api.route('/<int:id>')
class DrugsDisplay(Resource):
    @api.doc('get_drugs_by_id')
    @api.expect(token_parser)
    @token_required
    def get(self, token_parser, id):
        drug = Drugs.query.filter_by(id=id).first()
        if not drug:
            return {'message': 'No drug found!'}
        type = Types.query.filter_by(id=drug.type_id).first()
        drug_data = {'id': drug.id,
                     'name': drug.name,
                     'summary': drug.summary,
                     'legal_status': drug.legal_status,
                     'drug_testing': drug.drug_testing,
                     'way_consuming': drug.way_consuming,
                     'desired_effect': drug.desired_effect,
                     'secondary_effect': drug.secondary_effect,
                     'risks_complications': drug.risks_complications,
                     'addiction': drug.addiction,
                     'risk_reduction_tips': drug.risk_reduction_tips,
                     'img': drug.img,
                     'type_id': drug.type_id,
                     'type_name': type.name}
        return {'drug': drug_data}


@api.route('/types/<int:id>')
class TypesById(Resource):
    @api.doc('list_drugs_by_types_id')
    @api.expect(token_parser)
    @token_required
    def get(self, token_parser, id):
        drugs = Drugs.query.filter_by(type_id=id).all()
        output = []
        for drug in drugs:
            type = Types.query.filter_by(id=drug.type_id).first()
            drug_data = {'id': drug.id,
                         'name': drug.name,
                         'summary': drug.summary,
                         'legal_status': drug.legal_status,
                         'drug_testing': drug.drug_testing,
                         'way_consuming': drug.way_consuming,
                         'desired_effect': drug.desired_effect,
                         'secondary_effect': drug.secondary_effect,
                         'risks_complications': drug.risks_complications,
                         'addiction': drug.addiction,
                         'risk_reduction_tips': drug.risk_reduction_tips,
                         'img': drug.img,
                         'type_id': drug.type_id,
                         'type_name': type.name}
            output.append(drug_data)
        return {'drugs': output}


@api.route('/types/')
class TypesAll(Resource):
    @api.doc('list_all_drugs_order_by_type')
    @api.expect(token_parser)
    @token_required
    def get(self, token_parser):
        types = Types.query.all()
        output_type = []
        for type in types:
            drugs = Drugs.query.filter_by(type_id=type.id).all()
            output_drugs = []
            for drug in drugs:
                drug_data = {'id': drug.id,
                             'name': drug.name,
                             'summary': drug.summary,
                             'legal_status': drug.legal_status,
                             'drug_testing': drug.drug_testing,
                             'way_consuming': drug.way_consuming,
                             'desired_effect': drug.desired_effect,
                             'secondary_effect': drug.secondary_effect,
                             'risks_complications': drug.risks_complications,
                             'addiction': drug.addiction,
                             'risk_reduction_tips': drug.risk_reduction_tips,
                             'img': drug.img,
                             'type_id': drug.type_id,
                             'type_name': type.name}
                output_drugs.append(drug_data)
            output_type.append({type.name: output_drugs})
        return {'drugs': output_type}
