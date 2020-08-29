from datetime import datetime
from . import db


"""
flask-sqlalchemy:
    常用数据类型：
        Integer	一个整数
        String (size)	有长度限制的字符串
        Text	一些较长的 unicode 文本
        DateTime	表示为 Python datetime 对象的 时间和日期
        Float	存储浮点值
        Boolean	存储布尔值
        PickleType	存储为一个持久化的 Python 对象
        LargeBinary	存储一个任意大的二进制数据
        Enum 枚举
        
    常用约束：
        primary_key（主键）、unique（不可重复）、default（默认值是多少）、nullable(是否能为空)、Index（索引）
        
    一对一（外建）：
        person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    
    一对多：
        # 一个人可以有多个邮箱地址
        class Person(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String(50))
            addresses = db.relationship('Address', backref='person', lazy='dynamic')
        
        class Address(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            email = db.Column(db.String(50))
            person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
          
    多对多（需要另外建一张表来表示两者之间的关系）：
        tags = db.Table('tags',
            db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
            db.Column('page_id', db.Integer, db.ForeignKey('page.id'))
        )
        
        class Page(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            tags = db.relationship('Tag', secondary=tags,
                backref=db.backref('pages', lazy='dynamic'))
        
        class Tag(db.Model):
            id = db.Column(db.Integer, primary_key=True)
    
    
    tips（一般需要完成__init__()和__repr__()两个方法）：
        class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True)
        email = db.Column(db.String(120), unique=True)
    
        def __init__(self, username, email):
            self.username = username
            self.email = email
    
        def __repr__(self):
            return '<User %r>' % self.username
"""
class BaseModel(object):
    """模型类的基类，为每个模型补充创建时间和更新时间"""
    # 记录创建的时间
    create_time = db.Column(db.DateTime, default=datetime.now)
    # 记录更新的时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class GoodsModel(BaseModel, db.Model):
    """商品模型"""
    __tablename__ = 'ishop_goods'
    id = db.Column(db.Integer, primary_key=True)  # 商品ID，主键
    is_activate = db.Column(db.Boolean, nullable=False, default=True)  # 该商品是否处于激活状态，默认激活
    good_name = db.Column(db.String(80), nullable=False)  # 商品名称
    good_index_url = db.Column(db.String(256), nullable=False)  # 商品主图路径
    good_price = db.Column(db.Float, nullable=False)  # 商品价格
    good_desc = db.Column(db.String(256), nullable=False)  # 商品简介
    good_desc_details = db.Column(db.Text)  # 商品详情
    good_cate = db.Column(db.Integer, db.ForeignKey('ishop_goods_cates.id'))  # 商品分类，一对一，用外建
    # 商品评价 lazy表示禁止自动查询，一对多关系，需要ForeignKey和relationship配合
    good_commons = db.relationship('CommonsModel', backref='goodsmodel', lazy='dynamic')
    is_good_in_zeros = db.Column(db.Boolean, nullable=False, default=False)
    good_zero = db.relationship('ZerosModel', backref='goodsmodel')
    is_good_in_together = db.Column(db.Boolean, nullable=False, default=False)
    good_together = db.relationship('TogethersModel', backref='goodsmodel')


class ZerosModel(BaseModel, db.Model):
    """0元购模型"""
    __tablename__ = 'ishop_zeros'
    id = db.Column(db.Integer, primary_key=True)
    good_id = db.Column(db.Integer, db.ForeignKey('ishop_goods.id'))
    # 0元购第N天发货(数字)
    zero_datetime = db.Column(db.Integer, default=0)
    # 0元购每天返还的金额
    zero_back_money = db.Column(db.Integer, default=0)
    zero_desc = db.Column(db.String(256), nullable=False)


class TogethersModel(BaseModel, db.Model):
    """团购模型"""
    __tablename__ = 'ishop_togethers'
    id = db.Column(db.Integer, primary_key=True)
    good_id = db.Column(db.Integer, db.ForeignKey('ishop_users.id'))
    together_date = db.Column(db.DateTime, nullable=False)
    together_count = db.Column(db.Integer, nullable=False, default=100)
    together_deadline = db.Column(db.DateTime, nullable=False)
    together_desc = db.Column(db.String(256), nullable=False)


class GoodsCates(BaseModel, db.Model):
    """商品分类模型"""
    __tablename__ = 'ishop_goods_cates'
    id = db.Column(db.Integer, primary_key=True)
    cate = db.Column(db.String(20), nullable=False)



class UsersModel(BaseModel, db.Model):
    """用户模型"""
    __tablename__ = 'ishop_users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), unique=True)
    user_passwd_hash = db.Column(db.String(128), nullable=False)
    user_mobile = db.Column(db.String(11), nullable=False, unique=True)
    user_real_name = db.Column(db.String(32))
    user_id_card = db.Column(db.String(20))
    user_avator_url = db.Column(db.String(128), default='/avator.png')
    user_money = db.Column(db.Float)
    user_commons = db.relationship('CommonsModel', backref='usersmodel')
    user_orders = db.relationship('OrdersModel', backref='usersmodel')
    user_addresses = db.relationship('UserAddress', backref='usersmodel')


class CommonsModel(BaseModel, db.Model):
    __tablename__ = 'ishop_commons'
    id = db.Column(db.Integer, primary_key=True)
    good_id = db.Column(db.Integer, db.ForeignKey('ishop_goods.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('ishop_users.id'))
    common = db.Column(db.String(256), nullable=False)


class UserLevels(BaseModel, db.Model):
    """用户等级"""
    __tablename__ = 'ishop_users_levels'
    id = db.Column(db.Integer, primary_key=True)
    level_name = db.Column(db.String(20), nullable=False, unique=True)
    level_require = db.Column(db.Integer, nullable=False, unique=True)


class UserAddress(BaseModel, db.Model):
    __tablename__ = 'ishop_users_address'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('ishop_users.id'))
    user_address = db.Column(db.String(256), nullable=False)


class OrdersModel(BaseModel, db.Model):
    """订单模型"""
    __tablename__ = 'ishop_orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('ishop_users.id'))
    good_id = db.Column(db.Integer, db.ForeignKey('ishop_goods.id'))
    # 发货的最后时间（需要计算）
    tracking_deadline = db.Column(db.DateTime)
    tracking_number = db.Column(db.String(64))  # 物流单号
    is_order_in_zeros = db.Column(db.Boolean, nullable=False, default=False)
    order_zero = db.Column(db.Integer, db.ForeignKey('ishop_zeros.id'))
    is_order_in_together = db.Column(db.Boolean, nullable=False, default=False)
    order_together = db.Column(db.Integer, db.ForeignKey('ishop_togethers.id'))

