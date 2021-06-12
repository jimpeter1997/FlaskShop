from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
import pymysql





db = SQLAlchemy()



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    print("app.config = ", app.config)
    db.init_app(app)

    from flaskmain import views
    print("-----------------------------------")
    print("from flaskmain import views")
    print("-----------------------------------")
    app.register_blueprint(views.admin_views, url_prefix="")
    pymysql.install_as_MySQLdb()
    print("app = ", app)
    print("dir(app) = ", dir(app))
    return app
