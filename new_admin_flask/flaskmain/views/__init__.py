from flask import Blueprint, render_template


# 创建蓝图对象
admin_views = Blueprint("views", __name__)

# 为什么写在这个地方?
from . import index
