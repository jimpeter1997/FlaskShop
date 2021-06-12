import redis


# 配置
class Config(object):
    """配置参数"""

    SECRET_KEY = "!@#$%^tgfdsddfghfjgkgf"
    # 设置连接数据库的URL
    user = 'root'
    password = 'qwe123'
    database = 'TSqlalchemy'
    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@127.0.0.1:3306/{}'.format(user, password, database)

    # 设置sqlalchemy自动更跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = True

    # 禁止自动提交数据处理
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False


class DevConfig(Config):
    DEBUG = True

    # redis数据库 用于保存session的
    # 详情查阅flask-session
    SESION_TYPE = "redis"
    REDIS_SESSION_HOST = '127.0.0.1'
    REDIS_SESSION_PORT = 6379
    REDIS_SESSION_DB = 1

    # 如果设置session的生命周期是否是会话期, 为True，则关闭浏览器session就失效
    # SESSION_PERMANENT = False
    # SESSION有效期，单位：秒
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24  # 保存一天
    # 是否对发送到浏览器上session的cookie值进行加密
    SESSION_USE_SIGNER = True
    # 保存到redis的session数的名称前缀
    SESSION_KEY_PREFIX = "session_from_shop_admin_"
    # session保存数据到redis时启用的链接对象
    SESSION_REDIS = redis.StrictRedis(
        host=REDIS_SESSION_HOST,
        port=REDIS_SESSION_PORT,
        db=REDIS_SESSION_DB
    )  # 用于连接redis的配置


class ProConfig(Config):
    DEBUG = False


config_map = {
    'dev': DevConfig,
    'pro': ProConfig
}
