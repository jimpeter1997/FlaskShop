from flask import Flask
from config import config_map
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_session import Session
from flask_wtf import CSRFProtect
from ishop import api_1_0


# 用app对象创建数据对象db
db = SQLAlchemy()
# 创建redis连接对象，初始化为None
redis_store = None

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
    CSRFProtect(app)
    # 注册蓝图
    app.register_blueprint(api_1_0.api,url_prefix="/api/v1.0")
    return app