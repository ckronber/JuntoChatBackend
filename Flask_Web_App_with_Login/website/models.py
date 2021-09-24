from enum import unique
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

EMAIL_LENGTH = PASS_LENGTH = NAME_LENGTH = 150
DATA_LENGTH = 10000

class Chat(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    message = db.Column(db.String(DATA_LENGTH))
    message_type = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone = True),default=func.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    users = db.relationship('Users')

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(EMAIL_LENGTH), unique = True) # max length, unique means only unique emails
    password = db.Column(db.String(PASS_LENGTH))
    first_name = db.Column(db.String(NAME_LENGTH))
    userName = db.Column(db.String(NAME_LENGTH),unique = True)
    chats = db.relationship('Chat')
    channels = db.relationship('Channel')
    userList = db.relationship('UserList')

class Channel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(NAME_LENGTH), unique = True)
    description = db.Column(db.String(NAME_LENGTH), unique = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class UserList(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    userName = db.Column(db.String(NAME_LENGTH),unique=True)
    firstName = db.Column(db.String(NAME_LENGTH))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Users(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    userName = db.Column(db.String(NAME_LENGTH),unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('chat.id'))