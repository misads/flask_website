from flask import Flask
from sqlalchemy.engine.url import make_url
from sqlalchemy_utils import database_exists, create_database
from app.views import views

def create_app(config='app.config.Config'):
    app = Flask(__name__)
    with app.app_context():
        app.config.from_object(config)
        from app.models import db, Strangers

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


        app.register_blueprint(views)
        return app




