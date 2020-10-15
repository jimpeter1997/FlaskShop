# 用于配置项目相关的信息
import redis

# 创建配置对象
class Config(object):
    JSON_AS_ASCII = False
    """配置信息"""
    SECRET_KEY = 'Github12345!@#$'

    # mysql数据库
    # 数据类型://登录账号:登录密码@数据库主机IP:数据库访问端口/数据库名称
    SQLALCHEMY_DATABASE_URI = 'mysql://root:qwe123@127.0.0.1:3306/webvideoDB'
    # 设置mysql的错误跟踪信息显示
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 打印每次模型操作对应的SQL语句
    # SQLALCHEMY_ECHO = True

    # redis数据库 用于静态页面和图片验证码的数字
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
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24  # 保存一天
    # 是否对发送到浏览器上session的cookie值进行加密
    SESSION_USE_SIGNER = True
    # 保存到redis的session数的名称前缀
    SESSION_KEY_PREFIX = "session_from_flask_main_"
    # session保存数据到redis时启用的链接对象
    SESSION_REDIS = redis.StrictRedis(host=REDIS_SESSION_HOST, port=REDIS_SESSION_PORT,
                                      db=REDIS_SESSION_DB)  # 用于连接redis的配置



class DevelopmentConfig(Config):
    """开发模式的配置信息"""
    DEBUG = True
    SAVE_PATH = '/home/video_nginx_config'


class ProductionConfig(Config):
    """生成环境配置信息"""
    pass

config_map = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig
}
