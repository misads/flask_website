# coding=utf-8
# encoding=utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import bcrypt_sha256
from app.utils import get_time_stamp

app = Flask(__name__)
app.config.from_object('app.config.Config')
db = SQLAlchemy()  # type: SQLAlchemy


class Strangers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(80))

    def __init__(self, time):
        self.time = time

    def __repr__(self):
        return "<Pages route {0}>".format(self.route)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    website = db.Column(db.String(128))
    nickname = db.Column(db.String(128))
    number = db.Column(db.String(32))
    team = db.Column(db.Integer)  # 外键
    extra_info = db.Column(db.String(32))
    banned = db.Column(db.Boolean, default=False)
    verified = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)
    join_time = db.Column(db.String(32), default=get_time_stamp())

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt_sha256.encrypt(str(password))

    def __repr__(self):
        return '<user %r>' % self.name

