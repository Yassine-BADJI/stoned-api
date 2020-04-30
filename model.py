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
