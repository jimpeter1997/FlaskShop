# 存在这个__init__.py文件说明这个是一个包
# 一般在这里处理一些初始化的信息
from flask import Flask
from config import config_map
# from exts import db
import pymysql
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


def create_app(config_name):
    """
    创建flask应用对象
    :param config_name: str类型，配置模式的名字：develop或者product
    :return:flask的app对象
    """
    # 创建flaks的app对象
    app = Flask(__name__)
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)
    db.init_app(app) # 第三放扩展
    from adminshop import views
    # 注册蓝图
    app.register_blueprint(views.admin_views, url_prefix="")
    pymysql.install_as_MySQLdb()
    return app



