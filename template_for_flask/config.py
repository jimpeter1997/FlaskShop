# 用于配置项目相关的信息
# 创建配置对象
class Config(object):
    JSON_AS_ASCII = False
    """配置信息"""
    SECRET_KEY = 'Github12345!@#$'

    # mysql数据库
    # 数据类型://登录账号:登录密码@数据库主机IP:数据库访问端口/数据库名称
    SQLALCHEMY_DATABASE_URI = 'mysql://root:qwe123@127.0.0.1:3306/testDB'
    # 设置mysql的错误跟踪信息显示
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 打印每次模型操作对应的SQL语句
    # SQLALCHEMY_ECHO = True



class DevelopmentConfig(Config):
    """开发模式的配置信息"""
    DEBUG = True


class ProductionConfig(Config):
    """生成环境配置信息"""
    pass

config_map = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig
}
