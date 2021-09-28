from enum import unique
from sqlalchemy.sql.functions import user
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

EMAIL_LENGTH = PASS_LENGTH = NAME_LENGTH = 150
DATA_LENGTH = 10000

class Note(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    data = db.Column(db.String(DATA_LENGTH))
    date = db.Column(db.DateTime(timezone = True),default=func.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"id: {self.id}: date: {self.date} user: {self.user_id}"

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(EMAIL_LENGTH), unique = True) # max length, unique means only unique emails
    password = db.Column(db.String(PASS_LENGTH))
    first_name = db.Column(db.String(NAME_LENGTH))
    notes = db.relationship('Note', backref='user',cascade = "all, delete, delete-orphan",lazy = 'dynamic')
    channels = db.relationship('Channel', backref = 'user', cascade = "all, delete, delete-orphan", lazy = 'dynamic')
    
    def __repr__(self):
        return f"id: {self.id}: email: {self.first_name} user: {self.email}"

class Channel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(NAME_LENGTH), unique = True)
    description = db.Column(db.String(NAME_LENGTH), unique = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"id: {self.id}: email: {self.name} user: {self.description}"

class Team(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(NAME_LENGTH), unique = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"id: {self.id}: email: {self.name}"