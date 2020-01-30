# coding=utf-8
# encoding=utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import bcrypt_sha256
from app.utils import get_time_stamp

app = Flask(__name__)
app.config.from_object('app.config.Config')
db = SQLAlchemy()  # type: SQLAlchemy


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    value = db.Column(db.String(32))
    time = db.Column(db.String(32))

    def __init__(self, name, value, time):
        self.name = name
        self.value = value
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


class Pages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auth_required = db.Column(db.Boolean)
    title = db.Column(db.String(128))
    route = db.Column(db.String(128), unique=True)
    html = db.Column(db.Text)
    draft = db.Column(db.Boolean)

    def __init__(self, title, route, html, draft=True, auth_required=False):
        self.title = title
        self.route = route
        self.html = html
        self.draft = draft
        self.auth_required = auth_required

    def __repr__(self):
        return "<Pages route {0}>".format(self.route)


class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # chal = db.Column(db.Integer, db.ForeignKey('challenges.id'))
    location = db.Column(db.Text)

    def __init__(self, location):
        self.location = location

    def __repr__(self):
        return "<File {0} for challenge {1}>".format(self.location, self.chal)