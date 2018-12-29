from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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
