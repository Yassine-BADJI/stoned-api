from sqlalchemy import ForeignKey

from extensions import db


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(80))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    age = db.Column(db.String(50))
    admin = db.Column(db.Boolean, default=False)


class Types(db.Model):
    """ Type Model for storing type related details """
    __tablename__ = "Types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    drugs = db.relationship('Drugs', backref='types')


class Drugs(db.Model):
    """ Drug Model for storing drug related details """
    __tablename__ = "Drugs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    summary = db.Column(db.Text())
    legal_status = db.Column(db.Text())
    drug_testing = db.Column(db.Text())
    way_consuming = db.Column(db.Text())
    desired_effect = db.Column(db.Text())
    secondary_effect = db.Column(db.Text())
    risks_complications = db.Column(db.Text())
    addiction = db.Column(db.Text())
    risk_reduction_tips = db.Column(db.Text())
    type_id = db.Column(db.Integer, ForeignKey("Types.id"), nullable=False)
