from flask import Flask
from config import config_map
from flask_sqlalchemy import SQLAlchemy
import redis
import logging
from logging.handlers import  RotatingFileHandler
from flask_session import Session
from flask_wtf import CSRFProtect
import pymysql
from .utils.commonstools import ReConverter




# 用app对象创建数据对象db
db = SQLAlchemy()
# 创建redis连接对象，初始化为None
redis_store = None



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



# 工厂模式
def create_app(config_name):
    """
    创建flask的应用对象
    :param config_name: str类型： 配置模式的名字("develop", "product")
    :return:
    """
    # 创建app对象
    app = Flask(__name__)
    # 根据配置模式的名字获取配置参数的类
    config_class = config_map.get(config_name)
    # todo: 这个config_class 可能为空
    # 把配置对象放入app中
    app.config.from_object(config_class)
    # 使用app初始化db
    db.init_app(app)

    # 正式初始化redis,保存静态页面的redis
    global redis_store
    redis_store = redis.StrictRedis(
        host=config_class.REDIS_STATIC_HOST,
        port=config_class.REDIS_STATIC_PORT,
        db=config_class.REDIS_STATIC_DB
    )

    # 利用flask-session，将session数据保存到redis中
    Session(app)

    # 为flask开启csrf防护
    # CSRFProtect(app)
    # 为什么在这个地方导入api_1_0？？？ 解决循环导入的问题。
    from ishop import api_1_0
    app.url_map.converters["re"] = ReConverter  # 将自定义的转换器注册到flask中
    # 注册蓝图
    app.register_blueprint(api_1_0.api,url_prefix="/api/v1.0")
    pymysql.install_as_MySQLdb()
    return app