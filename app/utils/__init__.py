# coding=utf-8
# encoding = utf-8

import os
import hashlib
from flask import current_app as app, request, redirect, url_for, session, render_template, abort, jsonify
from .misc_utils import *
from .helper import *
from .decorators import *


def sha512(string):
    return hashlib.sha512(string).hexdigest()


def init_errors(app):
    @app.errorhandler(404)
    def page_not_found(error):
        if 'The requested URL was not found on the server.' in error.description:
            error.description = u'该页无法访问'
        return render_template('errors/404.html', error=error.description), 404

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', error=error.description), 403


def init_utils(app):
    @app.context_processor
    def inject_user():
        if session:
            return dict(session)
        return dict()

    @app.before_request
    def csrf():
        try:
            func = app.view_functions[request.endpoint]
        except KeyError:
            abort(404)
        if hasattr(func, '_bypass_csrf'):
            return
        if not session.get('nonce'):
            session['nonce'] = sha512(os.urandom(10))
        if request.method == "POST":
            if session['nonce'] != request.form.get('nonce'):
                return jsonify([str(session['nonce'])])

    @app.before_request
    def disable_jinja_cache():
        app.jinja_env.cache = {}
