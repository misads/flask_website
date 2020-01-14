from app.models import db, Strangers, Users
from flask import session


def authed():
    return bool(session.get('id', False))
