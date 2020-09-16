from . import api
from flask import current_app, request, jsonify, session
import re
from ishop import redis_store, db
from ishop.models import UsersModel
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
"""
注册相关
"""


# 注册 POST: url:/api/v1.0/users/register
@api.route("/users/register", methods=['POST'])
def register():
    """注册api
    请求方法：POST
    请求地址：/api/v1.0/users/register
    参数格式：json
    参数内容：    phoneNumber： 电话号码
                phoneCode： 短信验证码
                password： 密码
                repeatPassword： 重复密码
    返回格式： json
    返回内容：
                resCode：0为成功，其他为错误码
                message：提示信息
                data： 返回内容（json）
    """
    # request.form.get("key", type=str, default=None)
    # 获取表单数据
    # request.args.get("key")
    # 获取get请求参数
    # request.values.get("key")
    # 获取所有参数
    # request.get_json()
    # 获取解析json数据格式
    post_request_dict = request.get_json()
    phone_number = post_request_dict.get("jsdata").get("phoneNumber")
    phone_code = post_request_dict.get("jsdata").get("phoneCode")
    password = post_request_dict.get("jsdata").get("password")
    password2 = post_request_dict.get("jsdata").get("repeatPassword")
    print("post_request_dict = ", post_request_dict)
    print("phone_number = ", phone_number)
    print("phone_code = ", phone_code)
    print("password = ", password)
    print("password2 = ", password2)

    # 判断数据完整性
    if not all([phone_number, phone_code, password, password2]):
        return jsonify(resCode='1', message="参数不完整")

    # 判断手机号格式是否正确
    if not re.match(r"1[345789]\d{9}", phone_number):
        return jsonify(resCode='1', message="手机号码格式不正确")

    # 判断两个密码是否一致
    if password != password2:
        return jsonify(resCode='1', message="两次密码输入不正确")
    # todo： 然后你只要对一个密码进行验证就可以了
    # 从redis中取出短信验证码
    try:
        redis_sms_codes = redis_store.get("sms_codes_{}".format(phone_number))
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(resCode="1", message="数据库错误，读取验证码失败")
    # 判断短信验证码是否过期
    if redis_sms_codes is None:
        return jsonify(resCode='1', message="短信验证码已经过期，请再次请求短信验证码")
    # 判断用户填写的短信验证码是否正确
    if redis_sms_codes.lower() == phone_code.lower():
        return jsonify(resCode='1', message="短信验证码不正确")
    # todo：删除redis中的短信验证码，防止重复使用验证，可删，可不删，关键看业务需求
    # try:
    #     redis_store.delete("sms_codes_{}".format(phone_number))
    # except Exception as e:
    #     current_app.logger.error(e)

    # 判断手机号码是否已经注册过
    # 为什么和下面的判断合并了？能少链接数据库就少链接数据库
    # try:
    #     user = UsersModel.query().filter_by(user_mobile=phone_number).first()
    # except Exception as e:
    #     current_app.logger.error(e)
    #     return jsonify(resCode='1', message="数据库异常，请管理查询")
    # else:
    #     if user is not None:
    #         return jsonify(resCode='1', message="该手机号码已经被注册了，请登录")
    # 保存用户的注册资料到数据库中
    user = UsersModel()
    user.user_name = phone_number
    user.user_mobile = phone_number
    user.user_passwd = password
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        # 表示手机好已经注册过了
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(resCode='1', message="手机号码已经存在，请直接登录")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(resCode='1', message="数据库错误，请联系管理员处理")
    # 保存登录状态到session中 todo: 写入之前先判断是否存在
    session['name'] = phone_number
    session["mobile"] = phone_number
    session["id"] = user.id
    # 返回结果
    return jsonify(resCode='0', message="注册成功")

# 登录 POST: url: /api/v1.0/users/login
@api.route('/sessions', methods=['POST'])
def login():
    # 获取参数
    req_dict = request.get_json()
    mobile = req_dict.get("jsdata").get("phoneNumber")
    passwd = req_dict.get("jsdata").get("password")
    print(mobile, passwd)
    # 校验参数
    # 参数完整性的校验
    if not all([mobile, passwd]):
        return jsonify(resCode="1", message="参数不完整")

    # 手机号格式
    if not re.match(r"1[34578]\d{9}", mobile):
        return jsonify(resCode='1', message="手机号格式错误")
    # 判断错误次数是否超过限制，如果超过限制，则返回
    # redis记录： “access_nums_请求的id”：次数
    user_ip = request.remote_addr  # 用户的IP
    # 从数据库中根据手机号查询用户的数据对象
    try:
        access_num = redis_store.get("access_nums_{}".format(user_ip))
    except Exception as e:
        current_app.logger.error(e)
    else:
        if access_num is not None and int(access_num) >= 6:
            return jsonify(resCode='1', message="尝试次数过多，请十分钟以后尝试")
    # 用数据库的密码与用户填写的密码进行对比验证
    try:
        user = UsersModel.query.filter_by(user_mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(resCode='1', message="获取用户信息失败，请联系管理员")

    if user is  None or not user.check_password(passwd):
        try:
            redis_store.incr("access_nums_{}".format(user_ip))
            redis_store.expire("access_nums_{}".format(user_ip), 10*60)
        except Exception as e:
            current_app.logger.error(e)

        return jsonify(resCode='1', message="用户名或者密码错误")
    # 如果验证相同成功，保存登录状态，在session中 todo: 写入之前先判断是否存在
    session['name'] = user.user_name
    session["mobile"] = user.user_mobile
    session["id"] = user.id
    # 如果验证失败，记录错误次数，返回信息
    return jsonify(resCode='0', message="登录成功")

"""
检测用户是否已经登录
"""
@api.route("/session", methods=["GET"])
def check_login():
    name = session.get('name')
    if name is not None:
        return jsonify(resCode='0', massage="已经登录了", data={"name":name})
    else:
        return jsonify(resCode='1', massage="没有登录")


@api.route("/session", methods=["DELETE"])
def logout():
    session.clear()
    return jsonify(resCode='0', massage="退出成功")


