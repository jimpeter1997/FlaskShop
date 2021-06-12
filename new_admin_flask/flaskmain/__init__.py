from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_map
import pymysql


db = SQLAlchemy()



def create_app(config_name):
    # 初始化 Falsk对象
    app = Flask(__name__)

    # 导入配置
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)

    # 绑定各种插件
    db.init_app(app)

    from flaskmain import views
    # 注册蓝图
    app.register_blueprint(views.admin_views, url_prefix="")

    pymysql.install_as_MySQLdb()
    # 返回APP对象
    return app
