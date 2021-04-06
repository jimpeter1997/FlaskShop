from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash



class BaseModel(object):
    """模型类的基类，为每个模型补充创建时间和更新时间"""
    # 记录创建的时间
    create_time = db.Column(db.DateTime, default=datetime.now)
    # 记录更新的时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

# # 一个用户，多个地址
# class TestUser(BaseModel, db.Model):
#     __tablename__ = 'test_user_out'
#     id = db.Column(db.Integer, primary_key=True)
#     user_name = db.Column(db.String(80), nullable=False, unique=True)
#     user_address = db.relationship(  # 一对多关系中，这个一中，这里使用relationship
#         'TestAddress',  # 填写一对多关系中，一的那个类名
#         backref='TestUser',  # 填写一对多关系中， 多的那个类名
#         lazy='dynamic'  # 如果你在获取数据的时候，想要对多的那一边的数据再进行一层过滤，那么这时候就可以考虑使用`lazy='dynamic'
#     )
#
# class TestAddress(BaseModel, db.Model):
#     __tablename__ = 'test_address_out'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('test_user_out.id'))  # 一对多关系中，这个一中使用ForeignKey，并填写表名.id
#     user_address = db.Column(db.String(120), nullable=False)

# 后台管理员表
class AdminUser(BaseModel, db.Model):
    __tablename__ = 'ishop_admin_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password_hash = db.Column(db.String(120), nullable=False)
    is_super_user = db.Column(db.Boolean, default=False)

    # 加上property装饰器后，会把函数作为属性，函数名就是属性名称：设置属性操作
    @property
    def password(self):
        """读取属性的函数行为"""
        # 函数的返回值会作为属性的返回值
        # return check_password_hash(self.user_passwd_hash)
        # return ArithmeticError("这个属性只能设置，不能读取")
        return self.password_hash

    # 对应设置属性操作：注意这个装饰器，必须是带有@property装饰器的函数名
    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    # # 把函数转化成一个属性 @property
    # def generate_password_hash(self, origin_password):
    #     """对密码进行加密"""
    #     self.user_passwd_hash = generate_password_hash(origin_password)
    def check_password(self, passwd):
        """
        检验密码的正确性
        """
        return check_password_hash(self.password_hash, passwd)


# 公司信息表
class CompanyInformation(BaseModel, db.Model):
    __tablename__ = 'ishop_company_infos'
    id = db.Column(db.Integer, primary_key=True)  # 这个字段要不要？
    # 公司基础信息
    company_name = db.Column(db.String(25), default='AlexHunter‘s Company')
    web_title = db.Column(db.String(128), default="AlexHunter网站标题")
    web_key_wrods = db.Column(db.String(128), default="AlexHunter网站关键词")
    web_description = db.Column(db.String(128), default='AlexHunter网站描述')
    web_copyright = db.Column(db.String(128), default='AlexHunter版权信息或者备案信息')
    # 容联云短信发送
    ronglianyun_accId = db.Column(db.String(128), default='AlexHunter容联云信息，必须去申请！')
    ronglianyun_accToken = db.Column(db.String(128), default='AlexHunter容联云信息，必须去申请！')
    ronglianyun_appId = db.Column(db.String(128), default='AlexHunter容联云信息，必须去申请！')
    # 七牛云图床信息
    qiniu_acess_key = db.Column(db.String(128), default='AlexHunter七牛云图床信息，必须去申请！')
    qiniu_secret_key = db.Column(db.String(128), default='AlexHunter七牛云图床信息，必须去申请！')


# 用户信息表
class UserInfo(BaseModel, db.Model):
    __tablename__ = 'ishop_user_infos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=True)
    # password = db.Column(db.String(128), nullable=False)  # 后面处理
    password_hash = db.Column(db.String(120), nullable=False)
    mobile = db.Column(db.String(11), nullable=False, unique=True)
    money = db.Column(db.Float, default=0)  # 糙，Float不精准，大商城用int
    avatar_url = db.Column(db.String(128), default='/avatar.png')
    addresses = db.relationship('Address', backref='UserInfo')
    # commons = db.Column()  # todo:评论，后面处理
    # orders = db.Column()  # todo:订单信息，后面处理

    # 用户等级，后面处理
    # 加上property装饰器后，会把函数作为属性，函数名就是属性名称：设置属性操作
    @property
    def password(self):
        """读取属性的函数行为"""
        # 函数的返回值会作为属性的返回值
        # return check_password_hash(self.user_passwd_hash)
        # return ArithmeticError("这个属性只能设置，不能读取")
        return self.password_hash

    # 对应设置属性操作：注意这个装饰器，必须是带有@property装饰器的函数名
    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    # # 把函数转化成一个属性 @property
    # def generate_password_hash(self, origin_password):
    #     """对密码进行加密"""
    #     self.user_passwd_hash = generate_password_hash(origin_password)
    def check_password(self, passwd):
        """
        检验密码的正确性
        """
        return check_password_hash(self.password_hash, passwd)


# 用户地址表
class Address(BaseModel, db.Model):
    __tablename__ = 'ishop_address_infos'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('ishop_user_infos.id'))
    is_primary_address = db.Column(db.Boolean, nullable=False, default=False)
    address = db.Column(db.String(256), nullable=False)


# 活动表
class Activity(BaseModel, db.Model):
    __tablename__ = 'ishop_activities'
    id = db.Column(db.Integer, primary_key=True)
    activity_name = db.Column(db.String(32))
    start_time = db.Column(db.DateTime, default=datetime.now)
    close_time = db.Column(db.DateTime)
    activity_desc = db.Column(db.String(256))
    # 折扣力度
    off_percent = db.Column(db.Integer)
    # 发货时间
    package_time = db.Column(db.DateTime)
    # 是否处于激活状态
    is_active = db.Column(db.Boolean, nullable=False, default=False)


# 商品分类表
class GoodsKinds(BaseModel, db.Model):
    __tablename__ = 'ishop_goods_kinds'
    id = db.Column(db.Integer, primary_key=True)
    goods_kind_name = db.Column(db.String(32), nullable=False, unique=True)
    goods_kind_index = db.Column(db.Integer, nullable=False, default=100)
    goods_in_kind = db.relationship('Goods', backref='GoodsKinds', lazy='dynamic')


# 商品表
class Goods(BaseModel, db.Model):
    __tablename__ = 'ishop_goods'
    id = db.Column(db.Integer, primary_key=True)
    good_kind_id = db.Column(db.Integer, db.ForeignKey('ishop_goods_kinds.id'))
    good_name = db.Column(db.String(256), nullable=False)
    good_price = db.Column(db.Float)
    good_desc = db.Column(db.Text)
