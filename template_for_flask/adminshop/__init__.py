# 存在这个__init__.py文件说明这个是一个包
# 一般在这里处理一些初始化的信息
from flask import Flask
from config import config_map
import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import CSRFProtect
import logging
from logging.handlers import  RotatingFileHandler  # 设置保存文件位置等信息


# 设置日志的记录等级
logging.basicConfig(level=logging.DEBUG)
# 创建日志记录器， 指明保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
# 创建日志记录的格式
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日志记录器
logging.getLogger().addHandler(file_log_handler)


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

    # 利用flask-session，将session数据保存到redis中
    Session(app)
    # 利用flask-wtf， 为flask提供scrf_token保护
    CSRFProtect(app)
    from adminshop import views
    # 注册蓝图
    app.register_blueprint(views.admin_views, url_prefix="")
    pymysql.install_as_MySQLdb()
    return app



