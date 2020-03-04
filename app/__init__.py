import os

from flask import Flask
from sqlalchemy.engine.url import make_url
from sqlalchemy_utils import database_exists, create_database

from app.utils import init_utils, init_errors
from app.views import views
from app.auth import auth

from app.admin import admin
from app.admin import pages
from app.admin import share

from jinja2 import FileSystemLoader


class ThemeLoader(FileSystemLoader):
    """Custom FileSystemLoader that switches themes based on the configuration value"""
    def __init__(self, searchpath, encoding='utf-8', followlinks=False):
        super(ThemeLoader, self).__init__(searchpath, encoding, followlinks)
        self.overriden_templates = {}

    def get_source(self, environment, template):
        # Check if the template has been overriden
        if template in self.overriden_templates:
            return self.overriden_templates[template], template, True

        # Check if the template requested is for the admin panel
        if template.startswith('admin/'):
            template = template[6:]  # Strip out admin/
            template = "/".join(['admin', 'templates', template])
            return super(ThemeLoader, self).get_source(environment, template)

        # Load regular theme data
        template = "/".join(['user', 'templates', template])
        return super(ThemeLoader, self).get_source(environment, template)


def create_app(config='app.config.Config'):
    app = Flask(__name__)
    with app.app_context():
        app.config.from_object(config)

        theme_loader = ThemeLoader(os.path.join(app.root_path, 'html'), followlinks=True)
        app.jinja_loader = theme_loader

        from app.models import db

        url = make_url(app.config['SQLALCHEMY_DATABASE_URI'])
        if url.drivername == 'postgres':
            url.drivername = 'postgresql'

        if url.drivername.startswith('mysql'):
            url.query['charset'] = 'utf8mb4'

        # Creates database if the database database does not exist
        if not database_exists(url):
            if url.drivername.startswith('mysql'):
                create_database(url, encoding='utf8mb4')
            else:
                create_database(url)

        # This allows any changes to the SQLALCHEMY_DATABASE_URI to get pushed back in
        # This is mostly so we can force MySQL's charset
        app.config['SQLALCHEMY_DATABASE_URI'] = str(url)
       
        
        # Register database
        db.app = app
        db.init_app(app)

        db.create_all()

        app.db = db

        init_utils(app)
        init_errors(app)

        app.register_blueprint(views)
        app.register_blueprint(auth)
        app.register_blueprint(admin)
        app.register_blueprint(pages)
        app.register_blueprint(share)

        return app




