from flask import Flask
from config import config_map
# 数据库
from flask_sqlalchemy import SQLAlchemy
# session: flask默认session,在浏览器中,不安全,必然用到
from flask_session import Session
# 防止跨域攻击,必然用到
from flask_wtf import CSRFProtect
import pymysql





db = SQLAlchemy()



def create_app(config_name):
    app = Flask(__name__)
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)
    db.init_app(app)

    Session(app)
    CSRFProtect(app)

    from flaskmain import views
    app.register_blueprint(views.admin_views, url_prefix="")
    pymysql.install_as_MySQLdb()
    return app
