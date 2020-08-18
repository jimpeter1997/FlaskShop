"""
单一文件下的情况，我们的目标是把单一的文件拆分成一个项目文件夹

"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import CSRFProtect
import redis


# 创建app对象
app = Flask(__name__)

# 创建配置对象
class Config(object):
    """配置信息"""
    DEBUG = True

    SECRET_KEY = 'Github12345!@#$'

    # mysql数据库
    # 数据类型://登录账号:登录密码@数据库主机IP:数据库访问端口/数据库名称
    SQLALCHEMY_DATABASE_URI = 'mysql://root:qwe123@127.0.0.1:3306/ishop'
    # 设置mysql的错误跟踪信息显示
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 打印每次模型操作对应的SQL语句
    # SQLALCHEMY_ECHO = True

    # redis数据库 用于静态页面
    REDIS_STATIC_HOST = "127.0.0.1"
    REDIS_STATIC_PORT = 6379
    REDIS_STATIC_DB = 0

    # redis数据库 用于session
    REDIS_SESSION_HOST = "127.0.0.1"
    REDIS_SESSION_PORT = 6379
    REDIS_SESSION_DB = 1

    # 把session保存到redis中
    # session存储方式为redis
    SESSION_TYPE = "redis"
    # 如果设置session的生命周期是否是会话期, 为True，则关闭浏览器session就失效
    # SESSION_PERMANENT = False
    # SESSION有效期，单位：秒
    PERMANENT_SESSION_LIFETIME = 86400
    # 是否对发送到浏览器上session的cookie值进行加密
    SESSION_USE_SIGNER = True
    # 保存到redis的session数的名称前缀
    # SESSION_KEY_PREFIX = "session:"
    # session保存数据到redis时启用的链接对象
    SESSION_REDIS = redis.StrictRedis(host=REDIS_SESSION_HOST, port=REDIS_SESSION_PORT, db=REDIS_SESSION_DB)  # 用于连接redis的配置


# 把配置对象放入app中
app.config.from_object(Config)

# 用app对象创建数据对象db
db = SQLAlchemy(app)

# 创建redis连接对象
redis_store = redis.StrictRedis(host=Config.REDIS_STATIC_HOST, port=Config.REDIS_STATIC_PORT, db=Config.REDIS_STATIC_DB)

# 利用flask-session，将session数据保存到redis中
Session(app)

# 为flask开启csrf防护
CSRFProtect(app)

# 视图函数
@app.route("/", methods=['GET', 'POST'])
def index():
    return "Hello Flask"

# 启动入口
if __name__ == '__main__':
    app.run()