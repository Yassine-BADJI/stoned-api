from flask_restplus import Namespace, Resource

from apis.comun import token_required
from core.drugs import get_all_drugs, get_drug_by, get_type_by, get_all_drugs_by, get_all_type

api = Namespace('drugs', description='Drugs path')


@api.route('/')
class DrugsAll(Resource):
    @api.doc(security='apikey')
    @token_required
    def get(self, current_user):
        drugs = get_all_drugs()
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
    @api.doc(security='apikey')
    @token_required
    def get(self, current_user, id):
        drug = get_drug_by('id', id)
        type = get_type_by('id', drug.type_id)
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
    @api.doc(security='apikey')
    @token_required
    def get(self, current_user, id):
        drugs = get_all_drugs_by('type_id', id)
        output = []
        for drug in drugs:
            type = get_type_by('id', drug.type_id)
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
    @api.doc(security='apikey')
    @token_required
    def get(self, current_user):
        types = get_all_type()
        output_type = []
        for type in types:
            drugs = get_all_drugs_by('type_id', type.id)
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
