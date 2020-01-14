import datetime
import os
import time

from flask import current_app as app, Blueprint, jsonify, render_template, abort, send_file, session
from flask.helpers import safe_join


from app.models import db, Strangers

views = Blueprint('views', __name__)


def getTimeStr(fmt="%Y/%m/%d %H:%M:%S", yearlength=4):
    timeStamp = int(time.time())
    dateArray = datetime.datetime.utcfromtimestamp(timeStamp)

    # timezone = 8
    # timezonetime = dateArray + datetime.timedelta(hours=timezone)
    otherStyleTime = dateArray.strftime(fmt)

    if yearlength == 2:
        otherStyleTime = otherStyleTime[2:]
    return otherStyleTime


@views.route('/')
@views.route('/index')
def index():
    # session.permanent = True
    return render_template('index.html')
    # response = {'strangers': []}
    # s_q = Strangers.query.all()
    # for row in s_q:
    #     response['strangers'].append(row.time)
    # return jsonify(response)


@views.route('/query')
def query():
    return render_template('query.html')


# @views.route('/login', methods=['GET', 'POST'])
# def login():
#     return render_template('login.html')


@views.route('/detect')
def detect():
    timestr = getTimeStr()
    newstranger = Strangers(timestr)
    db.session.add(newstranger)
    db.session.commit()
    return timestr


@views.route('/deleteall')
def deleteall():
    Strangers.query.delete()
    db.session.commit()
    return 'succeed'


@views.route('/html/user/static/<path:path>')
def themes_handler(path):
    filename = safe_join(app.root_path, 'html', 'user', 'static', path)
    if os.path.isfile(filename):
        return send_file(filename)
    else:
        abort(404)
