from model import Drugs


def get_all_drugs():
    return Drugs.query.all()


def get_drug_by(search, value):
    kwargs = {search: value}
    return Drugs.query.filter_by(**kwargs).first()
