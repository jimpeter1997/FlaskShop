from . import db
from datetime import datetime


class BaseModel(object):
    """模型类的基类，为每个模型补充创建时间和更新时间"""
    # 记录创建的时间
    create_time = db.Column(db.DateTime, default=datetime.now)
    # 记录更新的时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

# 一个用户，多个地址
class TestUser(BaseModel, db.Model):
    __tablename__ = 'test_user_out'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), nullable=False, unique=True)
    user_address = db.relationship(  # 一对多关系中，这个一中，这里使用relationship
        'TestAddress',  # 填写一对多关系中，一的那个类名
        backref='TestUser',  # 填写一对多关系中， 多的那个类名
        lazy='dynamic'  # 如果你在获取数据的时候，想要对多的那一边的数据再进行一层过滤，那么这时候就可以考虑使用`lazy='dynamic'
    )

class TestAddress(BaseModel, db.Model):
    __tablename__ = 'test_address_out'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('test_user_out.id'))  # 一对多关系中，这个一中使用ForeignKey，并填写表名.id
    user_address = db.Column(db.String(120), nullable=False)
