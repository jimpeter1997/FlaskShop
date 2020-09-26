from . import db
from datetime import datetime


class BaseModel(object):
    """模型类的基类，为每个模型补充创建时间和更新时间"""
    # 记录创建的时间
    create_time = db.Column(db.DateTime, default=datetime.now)
    # 记录更新的时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class TestUser(BaseModel, db.Model):
    __tablename__ = 'test_user_out'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), nullable=False, unique=True)
    user_address = db.relationship('TestAddress', backref='TestUser', lazy='dynamic')

class TestAddress(BaseModel, db.Model):
    __tablename__ = 'test_address_out'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('test_user_out.id'))
    user_address = db.Column(db.String(120), nullable=False)