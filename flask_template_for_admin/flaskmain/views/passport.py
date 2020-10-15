from . import flask_views
from flask import render_template, current_app, redirect, url_for, request, flash,session
# from flaskmain.models import TestUser
from flaskmain.models import AdminUsers
import os
import re
from flaskmain.forms import AdminUserForm
from flaskmain.utils.commons import login_required
from .image_code import get_image_number


# @admin_views.route('/test', methods=['GET'])
# def test():
#     return 'test flask'
# @admin_views.route('test')
# def test():
#     print(current_app.config.get("SAVE_PATH"))
#     user = TestUser.query.filter_by(id=1).first()
#     print("user.user_address.first() = ", user.user_address.first())
#     print("user.user_address.all() = ", user.user_address.all())
#     # print("TestUser.query.filter_by(id=1).first().parent = ", TestUser.query.filter_by(id=1).first().parent)
#     # print("TestUser.query.filter_by(id=1).first().children = ", TestUser.query.filter_by(id=1).first().children)
#     print("用户地址 ：", user.user_address.all())
#     current_app.logger.error("测试错误")
#     addresses = []
#     for temp in user.user_address.all():
#         print("temp:", temp.user_address)
#         addresses.append(temp.user_address)
#     print(addresses)
#     context = {
#         'title': "测试标题",
#         'hinfo': "你好呀",
#         'user_name':user.user_name,
#         'addresses': addresses
#     }
#     return render_template('base.html', context=context)

@flask_views.route('/test_db')
def test_db():
    user = AdminUsers.query.filter_by(id=1).first()
    if user == None:
        return 'There is no AdminUser !'
    else:
        return user.username


@flask_views.route('/', methods=['GET', 'POST'])
# 没有使用login_manager的版本
@flask_views.route('/login', methods=['GET', 'POST'])
def login():
    form = AdminUserForm()
    context = {
        'title': '登录页面'
    }
    if request.method == 'POST':
        print('I am POST！！！！！！！')
        print(request.form.get('username'))
        print(request.form.get('password'))
        print(request.form.get('uuid'))
        print(request.form.get('imagenumber'))
        username = request.form.get('username')
        password = request.form.get('password')
        imagenumber = request.form.get('imagenumber')
        uuid = request.form.get('uuid')
        # 判断参数是否完整
        if not all([username, password, imagenumber, uuid]):
            # 此时参数不完整
            flash('参数不完整！')
            return render_template('/login.html', context=context, form=form)
        # 判断用户名是否包含特殊字符
        if re.search(r'[?*/\\<>:"|]', username) is not None:
            flash("用户名不能包含特殊字符")
            return render_template('/login.html', context=context, form=form)
        print("我的错在： uuid", uuid)
        image_number_in_redis = get_image_number(uuid)
        if image_number_in_redis == None:
            # 这边涉及到去数据库取数据，但是这个方法在读取数据库出错的情况下，会返回None，所以这边没有用try，直接用返回值来判断
            flash("发生未知错误，刷新后重试")
            return render_template('/login.html', context=context, form=form)
        print("image_number_in_redis = ", image_number_in_redis)
        print('imagenumber = ', imagenumber)
        if image_number_in_redis.lower() != imagenumber.lower():
            flash("验证码错误")
            return render_template('/login.html', context=context, form=form)

        try:
            user = AdminUsers.query.filter_by(username=username).first()
        except Exception as e:
            current_app.logger.error(e)
            flash("数据库异常，请联系管理员")
            return render_template('/login.html', context=context, form=form)

        if user is None or not user.check_password(password):
            flash("用户名不存在，或者密码错误")
            return render_template('/login.html', context=context, form=form)

        print("都对")
        session['id'] = user.id
        session['username'] = user.username
        print("开始跳转")
        # session['is_super_user'] = user.is_super_user
        return redirect(url_for('views.index'))


    return render_template('/login.html', context=context, form= form)


# 不使用login_manager的版本
@flask_views.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('views.login'))

# 后台首页
@flask_views.route('index')
@login_required
def index():
    return render_template('index.html')
