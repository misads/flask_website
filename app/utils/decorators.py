from flask import request, redirect, url_for, session, abort
import functools


def admins_only(f):
    """
    Decorator that requires the user to be authenticated and an admin
    :param f:
    :return:
    """
    @functools.wraps(f)
    def admins_only_wrapper(*args, **kwargs):
        if session.get('admin'):
            return f(*args, **kwargs)
        else:
            return redirect(url_for('auth.login', next=request.path))

    return admins_only_wrapper