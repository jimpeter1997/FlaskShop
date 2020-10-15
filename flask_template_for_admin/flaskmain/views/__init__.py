from flask import Blueprint


# 创建蓝图对象
flask_views = Blueprint("views", __name__)
# 导入蓝图的视图函数
from . import passport, image_code
