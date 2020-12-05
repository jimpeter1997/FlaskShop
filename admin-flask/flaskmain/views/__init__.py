from flask import Blueprint, render_template
from flask_wtf.csrf import generate_csrf


# 创建蓝图对象
admin_views = Blueprint("views", __name__)
# 导入蓝图的视图函数
from . import passport, image_code, admin, clients, goods



# 请求钩子
@admin_views.after_request
def after_request(response):
    # 调用函数生成 csrf_token
    csrf_token = generate_csrf()
    # 通过 cookie 将值传给前端
    response.set_cookie("csrf_token", csrf_token)
    return response



@admin_views.app_errorhandler(404)
def handler_404_error(error):  # 必须接受一个参数，名称随意
    """自定义的处理错误的方法"""
    # 这个函数的返回值会是前端用户看到的结果
    context = {
        'title': "错误页面"
    }
    if error:
        return render_template('404.html', error=error, context=context)
    else:
        return render_template('404.html', error="当前页面没有找到，已记录在日志，请联系管理员处理", context=context)
