from flask import Blueprint


# 创建蓝图对象
admin_views = Blueprint("views", __name__)

from . import index_test
