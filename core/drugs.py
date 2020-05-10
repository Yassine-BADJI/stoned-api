from werkzeug.exceptions import BadRequest

from model import Drugs, Types


def check_if_exist(data):
    if not data:
        raise BadRequest('No drug or type found!')


def get_all_drugs():
    return Drugs.query.all()


def get_all_drugs_by(search, value):
    kwargs = {search: value}
    return Drugs.query.filter_by(**kwargs).all()


def get_drug_by(search, value):
    kwargs = {search: value}
    drug = Drugs.query.filter_by(**kwargs).first()
    check_if_exist(drug)
    return drug


def get_all_type():
    return Types.query.all()


def get_type_by(search, value):
    kwargs = {search: value}
    type = Types.query.filter_by(**kwargs).first()
    check_if_exist(type)
    return type
