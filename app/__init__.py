from pathlib import Path

from flask import Flask

from app.config import Config
from app.extensions import bcrypt, csrf, db, login_manager


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)

    @app.get("/")
    def hello_world():
        return "Hello World"

    return app
