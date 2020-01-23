from app.models import db, Users
from flask import session


def authed():
    return bool(session.get('id', False))