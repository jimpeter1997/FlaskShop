# 配置
class Config(object):
    """配置参数"""
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
