import datetime
import os
import time

from flask import current_app as app, Blueprint, jsonify, render_template, abort, send_file, session, request, redirect
from flask.helpers import safe_join
from app import utils
from app.utils import admins_only

from app.models import db, Data, Pages, Files

pages = Blueprint('pages', __name__)


@pages.route('/admin/new_page')
@admins_only
def new_page():
    return redirect('/admin/pages?operation=create')


@pages.route('/admin/pages', methods=['GET', 'POST'])
@admins_only
def admin_pages_view():
    page_id = request.args.get('id')
    page_op = request.args.get('operation')

    if request.method == 'GET' and page_op == 'preview':
        page = Pages.query.filter_by(id=page_id).first_or_404()
        return render_template('admin/preview_page.html', content=page.html)

    if request.method == 'GET' and page_op == 'create':
        return render_template('admin/new_page.html')

    if page_id and request.method == 'GET':
        page = Pages.query.filter_by(id=page_id).first()
        return render_template('admin/new_page.html', page=page)

    if request.method == 'POST':
        page_form_id = request.form.get('id')
        title = request.form['title']
        html = request.form['html']
        route = request.form['route'].lstrip('/')
        auth_required = 'auth_required' in request.form

        if page_op == 'preview':
            page = Pages(title, route, html, draft=False)
            return render_template('admin/preview_page.html', content=page.html)

        page = Pages.query.filter_by(id=page_form_id).first()

        errors = []
        if not route:
            errors.append('Missing URL route')

        if errors:
            page = Pages(title, html, route)
            return render_template('/admin/new_page.html', page=page)

        if page:
            page.title = title
            page.route = route
            page.html = html
            page.auth_required = auth_required

            if page_op == 'publish':
                page.draft = False

            db.session.commit()

            data = {
                'result': 'success',
                'operation': page_op,
                'page': {
                    'id': page.id,
                    'route': page.route,
                    'title': page.title
                }
            }

            # db.session.close()
            # cache.clear()
            return jsonify(data)

        if page_op == 'publish':
            page = Pages(title, route, html, draft=False, auth_required=auth_required)
        elif page_op == 'save':
            page = Pages(title, route, html, auth_required=auth_required)

        p_q = Pages.query.filter_by(route=route).first()
        if p_q:
            return jsonify('route existed.')

        db.session.add(page)
        db.session.commit()

        data = {
            'result': 'success',
            'operation': page_op,
            'page': {
                'id': page.id,
                'route': page.route,
                'title': page.title
            }
        }

        # db.session.close()
        # cache.clear()

        return jsonify(data)

    pages = Pages.query.all()
    return render_template('admin/pages.html', pages=pages)


@pages.route('/admin/pages/delete', methods=['POST'])
@admins_only
def delete_page():
    id = request.form['id']
    page = Pages.query.filter_by(id=id).first_or_404()
    db.session.delete(page)
    db.session.commit()
    return '1'


@pages.route('/admin/pages/help', methods=['GET'])
@admins_only
def page_help():
    return render_template('admin/page_help.html')


@pages.route('/admin/media', methods=['GET', 'POST'])
@admins_only
def admin_pages_media():
    if request.method == 'POST':
        files = request.files.getlist('files[]')

        uploaded = []
        for f in files:
            data = utils.upload_file(file=f)
            if data:
                uploaded.append({'id': data[0], 'location': data[1]})
        return jsonify({'results': uploaded})
    elif request.method == 'DELETE':
        file_ids = request.form.getlist('file_ids[]')
        for file_id in file_ids:
            utils.delete_file(file_id)
        return True
    else:
        files = [{'id': f.id, 'location': f.location} for f in Files.query.all()]
        return jsonify({'results': files})

