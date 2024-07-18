from flask import Flask

from app.config import DevelopmentConfig, TestConfig
from app.core import db, init_app
from app.routes import main


def create_app(config_name="development"):
    app = Flask(__name__)
    if config_name == "development":
        app.config.from_object(DevelopmentConfig)
    elif config_name == "test":
        app.config.from_object(TestConfig)
    else:
        raise ValueError("Invalid configuration name")

    app.register_blueprint(main)

    init_app(app)

    with app.app_context():
        db.create_all()

    return app
