from  flaskr.db import db
from sqlalchemy.ext.associationproxy import association_proxy

class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(255))
    name = db.Column(db.String(255))
    role = db.Column(db.String(255))

    password_hash = db.Column(db.String(255), nullable=False)
    requested_objects_id = association_proxy('requests', 'object_id')

class ObjectModel(db.Model):
    __tablename__ = 'object'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    rooms = db.Column(db.Integer)
    size = db.Column(db.Integer)
    description = db.Column(db.Text)
    image_name = db.Column(db.String(255))

class RequestModels(db.Model):
    __tablename__ = 'request'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('UserModel',
        backref=db.backref('requests', lazy='dynamic'))
    object_id = db.Column(db.Integer, db.ForeignKey('object.id'))
    object = db.relationship('ObjectModel',
        backref=db.backref('requests', lazy='dynamic',cascade="all,delete",))

    __table_args__ = (db.UniqueConstraint('user_id', 'object_id', name='_user_object_'),)
