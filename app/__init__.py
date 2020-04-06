from flask import Flask
from flask_migrate import Migrate, upgrade
from sqlalchemy.engine.url import make_url
from sqlalchemy_utils import database_exists, create_database

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
    return app
