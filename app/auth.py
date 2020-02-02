import os

from flask import current_app as app, Blueprint, jsonify, render_template, abort, send_file, session, request, redirect
from app import utils
from app.models import db, Users
from passlib.hash import bcrypt_sha256

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    errors = []
    if not username:
        errors.append('Username can not be empty.')
    if not email:
        errors.append('Email can not be empty.')
    if not password:
        errors.append('Password can not be empty.')

    if len(errors) > 0:
        return jsonify(errors)

    username = username.strip()
    email = email.strip()

    forbidden_list = ['root', 'system', 'username', 'name', 'team', 'user']

    name_too_short = 0 < len(username) < 3
    name_empty = len(username) == 0
    name_too_long = len(username) > 16
    invalid_name = username in forbidden_list
    invalid_email = not utils.check_email_format(email)
    invalid_username = utils.check_email_format(username)
    username_existed = Users.query.add_columns('name', 'id').filter_by(name=username).first()
    email_existed = Users.query.add_columns('email', 'id').filter_by(email=email).first()
    pass_too_short = 0 < len(password) < 5
    pass_too_long = len(password) > 128

    errors = []
    errors_info = {
        'Username can not be shorter than 3 characters.': name_too_short,
        'Username can not be empty.': name_empty,
        'Username can not be longer than 16 characters.': name_too_long,
        'Illegal username.': invalid_name,
        'Username can not be an email format.': invalid_username,
        'Invalid email.': invalid_email,
        'Username has been taken.': username_existed,
        'Email has been taken.': email_existed,
        'Password can not be shorter than 5 characters.': pass_too_short,
        'Password can not be longer than 128 characters.': pass_too_long,
    }
    for msg in errors_info:
        if errors_info[msg]:
            errors.append(msg)

    if len(errors) > 0:
        return jsonify(errors)

    with app.app_context():
        user = Users(username, email.lower(), password)
        db.session.add(user)
        db.session.commit()
        db.session.flush()

        session['username'] = user.name
        session['id'] = user.id
        session['admin'] = user.admin
        session['nonce'] = utils.sha512(os.urandom(10))

    return jsonify([])


@auth.route('/login', methods=['GET'])
def login_page():
    if utils.authed():
        return render_template('index.html')
    next = request.args.get('next')

    return render_template('index.html', login=True, url=next)


@auth.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    errors = []
    if not username:
        errors.append('Username can not be empty.')
    if not password:
        errors.append('Password can not be empty.')

    if len(errors) > 0:
        return jsonify(errors)

    if utils.check_email_format(username) is True:
        user = Users.query.filter_by(email=username).first()
    else:
        user = Users.query.filter_by(name=username).first()

    if user:
        if bcrypt_sha256.verify(password, user.password):
            try:
                session.regenerate()  # NO SESSION FIXATION FOR YOU
            except:
                pass  # TODO: Some session objects don't implement regenerate :(

            session['username'] = user.name
            session['id'] = user.id
            session['admin'] = user.admin
            session['nonce'] = utils.sha512(os.urandom(10))
            db.session.close()
        else:
            return jsonify(['Invalid password.'])
    else:
        return jsonify(['Username not existed.'])

    return jsonify([])


@auth.route('/logout')
def logout():
    if utils.authed():
        session.clear()
    return redirect('/')
