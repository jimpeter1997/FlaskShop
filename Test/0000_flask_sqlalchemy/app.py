from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)

# 配置
class Config(object):
    """配置参数"""
    # 设置连接数据库的URL
    user = 'root'
    password = 'qwe123'
    database = 'TSqlalchemy'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@127.0.0.1:3306/{}'.format(user, password, database)

    # 设置sqlalchemy自动更跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 查询时会显示原始SQL语句
    app.config['SQLALCHEMY_ECHO'] = True

    # 禁止自动提交数据处理
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False

# 读取配置
app.config.from_object(Config)

# 创建数据库sqlalchemy工具对象
db = SQLAlchemy(app)


# 数据模型
class Role(db.Model):
    # 定义表名
    __tablename__ = 'roles'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User',backref='role') # 反推与role关联的多个User模型对象

class User(db.Model):
    # 定义表名
    __tablename__ = 'users'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64),unique=True)
    pswd = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id')) # 设置外键

# 视图函数
@app.route("/")
def index():
    pass

# 程序启动入口
if __name__ == '__main__':

    # 删除所有表
    db.drop_all()

    # 创建所有表
    db.create_all()
