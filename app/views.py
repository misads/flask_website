import datetime
import time

from flask import Blueprint, jsonify

from app.models import db, Strangers

views = Blueprint('views', __name__)


def getTimeStr(fmt="%Y/%m/%d %H:%M:%S", yearlength=4):
    timeStamp = int(time.time())
    dateArray = datetime.datetime.utcfromtimestamp(timeStamp)

    #timezone = 8
    #timezonetime = dateArray + datetime.timedelta(hours=timezone)
    otherStyleTime = dateArray.strftime(fmt)

    if yearlength == 2:
        otherStyleTime = otherStyleTime[2:]
    return otherStyleTime


@views.route('/')
@views.route('/index')
def index():
    response = {'strangers': []}
    s_q = Strangers.query.all()
    for row in s_q:
        response['strangers'].append(row.time)
    return jsonify(response)


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
