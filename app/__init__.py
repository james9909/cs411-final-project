from flask import Flask, render_template, session
from flask_migrate import Migrate, upgrade
from sqlalchemy.engine.url import make_url
from sqlalchemy_utils import database_exists, create_database
from pymongo import MongoClient

from app import api, views
from app.config import Config
from app.models import db

migrate = Migrate()

def create_app(config=Config()):
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    with app.app_context():
        app.config.from_object(config)
        db.init_app(app)
        migrate.init_app(app, db)

        url = make_url(app.config["SQLALCHEMY_DATABASE_URI"])
        url.query["charset"] = "utf8mb4"
        if not database_exists(url):
            create_database(url, encoding="utf8mb4")
            if len(db.engine.table_names()) == 0:
                   upgrade()

        app.db = db
        app.mongo_client = MongoClient(app.config["MONGODB_DATABASE_URI"])
        app.mongo_client.server_info()

        @app.context_processor
        def inject_user():
            return dict(user=session)

        app.register_blueprint(views.blueprint, url_prefix="/")
        app.register_blueprint(api.user.blueprint, url_prefix="/api/user")
        app.register_blueprint(api.airbnb.blueprint, url_prefix="/api/airbnbs")
        app.register_blueprint(api.attractions.blueprint, url_prefix="/api/attractions")
        app.register_blueprint(api.restaurants.blueprint, url_prefix="/api/restaurants")
    return app
