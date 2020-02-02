import datetime
import os
import time

from flask import current_app as app, Blueprint, jsonify, render_template, abort, send_file, session, request, redirect
from flask.helpers import safe_join
from app import utils
from app.utils import admins_only

from app.models import db, Data, Pages, Files

admin = Blueprint('admin', __name__)


@admin.route('/admin')
@admins_only
def admin_index():
    return render_template('admin/admin.html')

