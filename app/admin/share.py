# encoding=utf-8
import datetime
import os
import pdb
import shutil
import time

from flask import current_app as app, Blueprint, jsonify, render_template, abort, send_file, session, request, redirect
from flask.helpers import safe_join
from app import utils
from app.utils import admins_only

from app.models import db, Data, Pages, Files
from werkzeug.utils import secure_filename

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

share = Blueprint('share', __name__)


@share.route('/admin/share/view/', methods=['GET'])
@share.route('/admin/share/view/<path:logs_dir>', methods=['GET'])
@admins_only
def share_view(logs_dir=''):

    file_ele_list = list()
    dir_ele_list = list()
    share_folder = os.path.join(app.root_path, app.config['SHARE_FOLDER'])
    if not logs_dir:
        logs_dir = ''
    cur_folder = safe_join(share_folder, logs_dir)

    cur_folder = cur_folder.encode()

    if not os.path.isdir(cur_folder):
        if os.path.isfile(cur_folder):
            return send_file(cur_folder)
        else:
            abort(404)
    path = os.listdir(cur_folder)
    for f in path:

        fullname = os.path.join(cur_folder, f)
        last_modify_time = os.path.getmtime(fullname)
        last_modify_time = utils.get_time_str(last_modify_time, fmt='%Y/%m/%d %H:%M:%S')
        if os.path.isfile(fullname):
            size = utils.format_size(os.path.getsize(fullname))
            file_ele_list.append({'is_dir': 0, 'filesize': size,
                                  'last_modify_time': last_modify_time,
                                  'url': '-', 'download_url': '-', 'fullname': f})
        if os.path.isdir(fullname):

            dir_ele_list.append({'is_dir': 1, 'filesize': u'文件夹',
                                 'last_modify_time': last_modify_time, 'url': '-', 'download_url': '-', 'fullname': f})

    url = '/%s/' % logs_dir if logs_dir else '/'
    if not logs_dir:
        navs = [('share/', '')]
    else:
        navs = [('share/', '')]
        cur = ''
        for i in url.split('/')[1:-1]:
            if not i:
                continue
            cur = os.path.join(cur, i)
            navs.append((i + '/', cur))

    return render_template('admin/share_view.html', ele_list=dir_ele_list + file_ele_list,
                           logs_dir=logs_dir, url=url, navs=navs)


# @share.route('/admin/share/delete', methods=['POST'])
# @admins_only
# def delete_page22():
#     path = request.form['path']
#     if not path:
#         return '0'
#     share_folder = os.path.join(app.root_path, app.config['SHARE_FOLDER'])
#     rm_file = safe_join(share_folder, path)
#     if os.path.isfile(rm_file):
#         os.remove(rm_file)
#     else:
#         return '0'
#     return '1'

@share.route('/admin/share/upload', methods=['POST'])
@admins_only
def upload_share():
    files = request.files.getlist('files[]')
    path = request.form['path']
    path = path.lstrip('/')

    share_folder = os.path.join(app.root_path, app.config['SHARE_FOLDER'])

    for f in files:
        filename = f.filename
        save_path = os.path.join(share_folder, path, filename)
        save_path = save_path.encode()

        utils.color_print(save_path, 3)

        if os.path.isfile(save_path):
            return jsonify([u'文件名已存在'])

        f.save(save_path)

    return jsonify([])


@share.route('/admin/share/delete', methods=['POST'])
@admins_only
def delete_share():
    path = request.form['path']
    if not path:
        return '0'
    path = path.lstrip('/')
    share_folder = os.path.join(app.root_path, app.config['SHARE_FOLDER'])
    rm_file = safe_join(share_folder, path)

    rm_file = rm_file.encode()

    if not os.path.exists(rm_file):
        return '0'
    if os.path.isfile(rm_file):
        os.remove(rm_file)
    else:
        shutil.rmtree(rm_file)
    return '1'


@share.route('/admin/share/rename', methods=['POST'])
@admins_only
def rename_share():
    path = request.form['path']
    name = request.form['name']
    if not path or not name:
        return jsonify(['Error'])

    path = path.lstrip('/')
    name = name.lstrip('/')

    share_folder = os.path.join(app.root_path, app.config['SHARE_FOLDER'])

    try:
        raw_file = safe_join(share_folder, path)
        rename_file = safe_join(share_folder, name)
    except:
        return jsonify(['文件名非法'])

    raw_file = raw_file.encode()
    rename_file = rename_file.encode()

    try:
        os.rename(raw_file, rename_file)
    except:
        return jsonify(['文件名非法'])

    return jsonify([])


@share.route('/admin/share/create', methods=['POST'])
@admins_only
def create_share():
    path = request.form['path']
    name = request.form['name']
    if not name:
        name = 'new_directory'
    if not path:
        return jsonify(['path not existed'])

    if ' ' in name:
        return jsonify([u'文件夹名中不能有空格'])

    path = path.lstrip('/')
    share_folder = os.path.join(app.root_path, app.config['SHARE_FOLDER'])
    try:
        new_dir = safe_join(share_folder, path, name)
    except:
        return jsonify([u'非法的目录名'])

    new_dir = new_dir.encode()

    # new_dir = new_dir.decode('utf-8')
    try:
        if os.path.exists(new_dir):
            return jsonify([u'文件夹已存在'])
        os.mkdir(new_dir)
    except:
        return jsonify([u'编码错误, 请使用英文路径后重试'])

    return jsonify([])
