# 设置全局数据库工具，避免多次实例化SQLAlchemy
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()