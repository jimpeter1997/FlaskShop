from . import admin_views
from flask import render_template, current_app, request, flash, url_for, session, redirect
from flaskmain.forms import AdminUserForm
import re
from .image_code import  get_image_number
from flaskmain.utils.common import login_required
from flaskmain.models import AdminUser


# 没有使用login_manager的版本
@admin_views.route('/login', methods=['GET', 'POST'])
@admin_views.route('/', methods=['GET', 'POST'])
def login():
    if session.get('id') is not None:
        return redirect(url_for('views.index'))
    form = AdminUserForm()
    context = {
        'title': '登录页面'
    }
    if request.method == 'POST':
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
            user = AdminUser.query.filter_by(username=username).first()
        except Exception as e:
            current_app.logger.error(e)
            flash("数据库异常，请联系管理员")
            return render_template('/login.html', context=context, form=form)

        print(user.username)
        print(password)
        print(user.check_password(password))

        if user is None or not user.check_password(password):
            flash("用户名不存在，或者密码错误")
            return render_template('/login.html', context=context, form=form)

        session['id'] = user.id
        session['username'] = user.username
        session['is_super_user'] = user.is_super_user
        return redirect(url_for('views.index'))


    return render_template('/login.html', context=context, form=form)



# 不使用login_manager的版本
@admin_views.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('views.login'))


@admin_views.route('/index', methods=['GET'])
@login_required
def index():
    context = {
        'title': "后台首页"
    }
    print("current_app.url_map = ", current_app.url_map)
    return render_template('/index.html', context=context)





# 不使用login_manager的版本
# @admin_views.route('/index', methods=['GET'])
# def index():
#     try:
#         username = session['username']
#         print('username1 = ', username)
#     except :
#         username = None
#
#     print('username2 = ', username)
#     if username == None:
#         return redirect(url_for('views.login'))
#
#     context = {
#         'title': '后台首页',
#         'username': session['username']
#     }
#     return render_template('/index.html', context=context)
