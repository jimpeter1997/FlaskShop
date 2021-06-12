from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
import pymysql





db = SQLAlchemy()



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    print("app.config = ", app.config)
    db.init_app(app=app)
    pymysql.install_as_MySQLdb()
    # db.drop_all()
    # db.create_all()

    return app
