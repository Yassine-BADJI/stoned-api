from werkzeug.exceptions import BadRequest

from model import Takes


def check_if_exist(take):
    if not take:
        raise BadRequest('No take(s) found')


def get_all_takes():
    return Takes.query.all()


def get_all_takes_by(search, value):
    kwargs = {search: value}
    takes = Takes.query.filter_by(**kwargs).all()
    check_if_exist(takes)
    return takes


def get_takes_by(search, value):
    kwargs = {search: value}
    take = Takes.query.filter_by(**kwargs).first()
    check_if_exist(take)
    return take


