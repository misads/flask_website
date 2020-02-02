import hashlib
import os

from app.models import db, Users
from flask import current_app as app, session

from app.models import db, Files
from werkzeug.utils import secure_filename


def authed():
    return bool(session.get('id', False))


def upload_file(file):
    filename = secure_filename(file.filename)

    if len(filename) <= 0:
        return False

    md5hash = hashlib.md5(os.urandom(64)).hexdigest()

    upload_folder = os.path.join(os.path.normpath(app.root_path), app.config['UPLOAD_FOLDER'])
    if not os.path.exists(os.path.join(upload_folder, md5hash)):
        os.makedirs(os.path.join(upload_folder, md5hash))

    file.save(os.path.join(upload_folder, md5hash, filename))
    db_f = Files((md5hash + '/' + filename))
    db.session.add(db_f)
    db.session.commit()
    return db_f.id, (md5hash + '/' + filename)
