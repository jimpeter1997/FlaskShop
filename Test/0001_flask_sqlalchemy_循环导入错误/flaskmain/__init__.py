from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy









def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    print("app.config = ", app.config)
    db = SQLAlchemy(app)

    return app
