import datetime
import os
import time
import json

from flask import current_app as app, Blueprint, jsonify, render_template, abort, send_file, session, request, redirect
from flask.helpers import safe_join
from pyecharts_javascripthon.api import TRANSLATOR

from app import utils

from app.models import db, Data, Files, Pages

views = Blueprint('views', __name__)


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


@views.route("/<path:template>")
def static_html(template):
    page = Pages.query.filter_by(route=template).first()
    if page is None:
        abort(404)
    else:
        if page.auth_required and utils.authed() is False:
            return redirect('/login')

        return render_template('page.html', content=page.html)


REMOTE_HOST = "/html/user/static/js/echarts"


@views.route('/graph')
def graph():
    from app.interface import get_graph
    kline = get_graph()
    return render_template('graph.html', url='/graph', myechart=kline.render_embed(),
                           host=REMOTE_HOST,
                           script_list=kline.get_js_dependencies(), chart_id=kline.chart_id)


@views.route('/g')
def g():
    from app.interface import get_graph
    kline = get_graph()
    snippet = TRANSLATOR.translate(kline.options).as_snippet()
    d = json.loads(snippet)
    return jsonify(d)


@views.route('/new')
def new_detect():
    requests = request.args
    if 'name' not in requests or 'value' not in requests:
        return jsonify([])

    name = requests['name']
    value = requests['value']
    timestr = utils.get_time_str(utils.get_time_stamp())
    name_q = Data.query.filter_by(name=name).first()
    status = 'Add'
    if name_q:
        status = 'Update'
        name_q.value = value
        name_q.time = timestr
        db.session.commit()
    else:
        new_data = Data(name, value, timestr)
        db.session.add(new_data)
        db.session.commit()
    return jsonify([status, name, value, timestr])


@views.route('/delete_all', methods=['GET'])
def delete_all():
    Data.query.delete()
    db.session.commit()
    return 'succeed'


@views.route('/files', defaults={'path': ''})
@views.route('/files/<path:path>')
def file_handler(path):
    f = Files.query.filter_by(location=path).first_or_404()

    upload_folder = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_file(safe_join(upload_folder, f.location))


@views.route('/html/user/static/<path:path>')
def themes_handler(path):
    filename = safe_join(app.root_path, 'html', 'user', 'static', path)
    if os.path.isfile(filename):
        return send_file(filename)
    else:
        abort(404)
