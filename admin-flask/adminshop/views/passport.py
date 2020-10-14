from . import admin_views
from flask import render_template, current_app, request, flash, url_for, session, redirect
from adminshop.models import TestUser, AdminUser
from adminshop.forms import AdminUserForm
from adminshop import login_manager
from flask_login import login_required, login_user, logout_user, current_user
import re
from . image_code import  get_image_number



@login_manager.user_loader
def user_loader(id):
    return AdminUser.query.filter_by(id=id).first()


# @admin_views.route('/test', methods=['GET'])
# def test():
#     return 'test flask'
@admin_views.route('test')
def test():
    user = TestUser.query.filter_by(id=1).first()
    print("user.user_address.first() = ", user.user_address.first())
    print("user.user_address.all() = ", user.user_address.all())
    # print("TestUser.query.filter_by(id=1).first().parent = ", TestUser.query.filter_by(id=1).first().parent)
    # print("TestUser.query.filter_by(id=1).first().children = ", TestUser.query.filter_by(id=1).first().children)
    print("用户地址 ：", user.user_address.all())
    current_app.logger.error("测试错误")
    addresses = []
    for temp in user.user_address.all():
        print("temp:", temp.user_address)
        addresses.append(temp.user_address)
    print(addresses)
    context = {
        'title': "测试标题",
        'hinfo': "你好呀",
        'user_name':user.user_name,
        'addresses': addresses
    }
    return render_template('base.html', context=context)


# 使用了login_manager的版本
@admin_views.route('/login', methods=['GET', 'POST'])
def login():
    # print("session['username'] = ", session['_user_id'])
    try:
        user_id = session['_user_id']
        # user_id = current_user.get(id)
    except:
        user_id = None

    if user_id is not None:
        return redirect(url_for('views.index'))
    # if current_user is not None:
    #     return redirect(url_for('views.index'))
    # try:
    #     user = current_user
    # except:
    #     user = None
    # if user is not None:
    #     return redirect(url_for('views.index'))
    form = AdminUserForm()
    context = {
            'title': '登录页面'
    }
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        uuid = request.form.get('uuid')
        image_number_from_web = request.form.get('imagenumber')
        # 判断参数是否完整
        if not all([username, password, uuid, image_number_from_web]):
            flash("参数不完整，请重新填写")
            return redirect(url_for('views.login'))
        # 判断图片验证码是否正确
        if image_number_from_web.lower() != get_image_number(uuid).lower():
            flash("验证码不正确，请刷新后重新尝试")
            return redirect(url_for('views.login'))
        # 判断username是否包含特殊字符
        if re.search(r'[?*/\\<>:"|]', username) is not None:
            flash("用户名不能包含特殊字符")
            return redirect(url_for('views.login'))
        # 获取user对象
        try:
            user = AdminUser.query.filter_by(username=username).first()
        except Exception as e:
            current_app.logger.error("数据库链接错误")
            flash("数据库错误，请联系管理员处理")
            return redirect(url_for('views.login'))
        # 判断用户是否存在，密码是否正确
        if user is None or not user.check_password(password):
            flash("用户名或者密码错误")
            return  redirect(url_for('views.login'))

        login_user(user)
        return redirect(url_for('views.index'))

    return render_template('/login.html', context=context, form=form)


# 没有使用login_manager的版本
# @admin_views.route('/login', methods=['GET', 'POST'])
# def login():
#     form = AdminUserForm()
#     context = {
#         'title': '登录页面'
#     }
#     if request.method == 'POST':
#         print('I am POST！！！！！！！')
#         print(request.form.get('username'))
#         print(request.form.get('password'))
#         print(request.form.get('uuid'))
#         print(request.form.get('imagenumber'))
#         username = request.form.get('username')
#         password = request.form.get('password')
#         imagenumber = request.form.get('imagenumber')
#         uuid = request.form.get('uuid')
#         # 判断参数是否完整
#         if not all([username, password, imagenumber, uuid]):
#             # 此时参数不完整
#             flash('参数不完整！')
#             return render_template('/login.html', context=context, form=form)
#         # 判断用户名是否包含特殊字符
#         if re.search(r'[?*/\\<>:"|]', username) is not None:
#             flash("用户名不能包含特殊字符")
#             return render_template('/login.html', context=context, form=form)
#
#         image_number_in_redis = get_image_number(uuid)
#         if image_number_in_redis == None:
#             # 这边涉及到去数据库取数据，但是这个方法在读取数据库出错的情况下，会返回None，所以这边没有用try，直接用返回值来判断
#             flash("发生未知错误，刷新后重试")
#             return render_template('/login.html', context=context, form=form)
#         print("image_number_in_redis = ", image_number_in_redis)
#         print('imagenumber = ', imagenumber)
#         if image_number_in_redis.lower() != imagenumber.lower():
#             flash("验证码错误")
#             return render_template('/login.html', context=context, form=form)
#
#         try:
#             user = AdminUser.query.filter_by(username=username).first()
#         except Exception as e:
#             current_app.logger.error(e)
#             flash("数据库异常，请联系管理员")
#             return render_template('/login.html', context=context, form=form)
#
#         if user is None or not user.check_password(password):
#             flash("用户名不存在，或者密码错误")
#             return render_template('/login.html', context=context, form=form)
#
#         session['id'] = user.id
#         session['username'] = user.username
#         session['is_super_user'] = user.is_super_user
#         return redirect(url_for('views.index'))
#
#
#     return render_template('/login.html', context=context, form= form)

@admin_views.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.login'))

# 不使用login_manager的版本
# @admin_views.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('views.login'))


@admin_views.route('/index', methods=['GET'])
@login_required
def index():
    print('current_user = ', current_user)
    print('current_user = ', current_user.id)
    print('current_user = ', current_user.username)
    print('current_user = ', current_user.password)
    print('current_user = ', current_user.is_super_user)
    print('session[_id] = ', session['_id'])
    print('session[_id] = ', session['_user_id'])
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