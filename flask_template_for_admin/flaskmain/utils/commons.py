from werkzeug.routing import BaseConverter
from flask import session, jsonify, g
import functools
import re
from flask import flash, redirect, url_for


# 自定义万能转换器（用正则表达式匹配）
class ReConverter(BaseConverter):
    def __init__(self, url_map, regex):
        # 调用父类的初始化方法
        super(ReConverter, self).__init__(url_map)
        # 保存正则表达式
        self.regex = regex


# 检查是否含有特殊字符
def is_string_validate(str):
    sub_str = re.sub(r'！@#￥%……&×;；=', "", str)
    if len(str) == len(sub_str):
        # 说明合法
        return False
    else:
        # 不合法
        return True


# 定义验证登录状态的装饰器
def login_required(view_func):
    @functools.wraps(view_func)  # 如果没有这个这个装饰器，那么set_user_avatar这个函数的，set_user_avatar.name会变成wrapper.name
    def wrapper(*args, **kwargs):
        # 判断用户的登录状态
        user_id = session.get("id")
        if user_id is not None:
            # g对象中保存，传递的信息
            g.user_id = user_id
            # 如果用户是登录状态，放行，直接执行视图函数
            return view_func(*args, **kwargs)
        else:
            # 如果用户非登录状态，拒绝，返回json，告诉前端去跳转(API形态)
            # return jsonify(resCode='2', message="用户未登录，前端需要跳转")
            # template模式
            flash('请先登录才能访问哦')
            return redirect(url_for('views.login'))
    return wrapper


"""
@login_required
def set_user_avatar():
    user_id = g.user_id  # 通过g对象就可以获取user_id
    pass
    return jsonify(...)

set_user_avatar()  -> warpper()
"""
