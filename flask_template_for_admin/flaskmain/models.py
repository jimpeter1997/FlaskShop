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
#         'TestAddress',  # 填写一对多关系中，多的那个类名
#         backref='TestUser',  # 填写一对多关系中， 多的那个类名
#         lazy='dynamic'  # 如果你在获取数据的时候，想要对多的那一边的数据再进行一层过滤，那么这时候就可以考虑使用`lazy='dynamic'
#     )
#
# class TestAddress(BaseModel, db.Model):
#     __tablename__ = 'test_address_out'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('test_user_out.id'))  # 一对多关系中，这个一中使用ForeignKey，并填写表名.id
#     user_address = db.Column(db.String(120), nullable=False)


# 管理员表
class AdminUsers(BaseModel, db.Model):
    __tablename__ = 'video_admin_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# 服务器信息表
class ServerIPs(BaseModel, db.Model):
    __tablename__ = 'video_server_ips'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    port = db.Column(db.Integer, nullable=False, default=22)
    nickname = db.Column(db.String(8), nullable=False, unique=True)
    website = db.relationship(
        'WebsiteInfos',
        backref='ServerIPs',
        lazy='dynamic'
    )


# 网站信息表
class WebsiteInfos(BaseModel, db.Model):
    __tablename__ = 'video_website_infos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.Integer, db.ForeignKey('video_server_ips.id'))
    url = db.Column(db.String(128), nullable=False)
    is_activate = db.Column(db.Boolean, default=True, nullable=False)
    title = db.Column(db.String(128))
    keywords = db.Column(db.String(128))
    description = db.Column(db.String(128))
    baidu_code = db.Column(db.String(256))  # 百度统计代码


# 联系方式
class ContactInfos(BaseModel, db.Model):
    __tablename__ = 'video_contact_infos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    way = db.Column(db.String(32), nullable=False)
    detail = db.Column(db.String(128), nullable=False)
