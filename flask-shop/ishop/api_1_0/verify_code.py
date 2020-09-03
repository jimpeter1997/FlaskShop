from . import api
from ishop.utils.captcha import Captcha
from ishop import redis_store, db
from flask import current_app, jsonify, make_response, request
from io import BytesIO
from ishop.models import UsersModel
from ishop.libs.ronglian_sms_sdk.SendMessage import CCP
import random


@api.route('/image_codes/<string:image_uuid>')
def get_image_code(image_uuid):
    """
    获取图片验证码
    : params: image_uuid: 验证码编号
    : return：  正常情况下 返回验证码图片
                异常情况下 返回json数据
    """
    text, img = Captcha.gene_code()
    # redis: 字符串、列表(数组)、哈希、set(zet)
    # 字符串：“key”： xxx
    # 哈希： image_condes: {"编号1"：“验证码文本1”，“编号2”：“验证码文本2”}： hset("image_condes","编号1"，“验证码文本1”)、hget()
    # 选择字符串类型
    # redis_store.set("image_code_%s".format(image_uuid), text)
    # redis_store.expire("image_code_code_%s".format(image_uuid), 5*60)
    try:
        redis_store.setex("image_code_{}".format(image_uuid), 5*60, text)
    except Exception as e:
        # 记录日志
        current_app.logger.error(e)
        # return jsonify(errno='504', massages="save image failed")
        return jsonify(resCode='504', massages="保存验证码图片失败")

    buf = BytesIO()
    img.save(buf, 'png')
    buf_str = buf.getvalue()

    # 返回图片
    resp = make_response(buf_str)
    resp.headers["Content-Type"] = "image/png"
    return resp


# GET  url: /apt/v1.0/sms_codes/<手机号码>?image_uuid=图片验证码UUID&image_code=图片验证码数据
@api.route('/sms_codes/<re(r"1[345789]\d{9}"):mobile>')
def get_sms_codes(mobile):
    """获取短信验证码"""
    # 1.获取参数
    image_uuid = request.args.get("image_uuid")
    image_code = request.args.get("image_code")
    # 1.1 校验参数     Q：为什么手机号码不校验了？A：看转换器re;
    #                 Q:为什么不对这两个数据进行更具体的校验？A因为他们不写入数据库
    if not all([image_uuid, image_code]):
        # 表示参数不完整
        return jsonify(resCode='1', message="参数不正确")
    # 2.校验参数
    # 2.1 从redis中取出数据
    try:
        real_image_code = redis_store.get("image_code_{}".format(image_uuid))
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(resCode='1', message="数据库异常")

    # 2.2 由于存在redis过期，或者本身uuid就是错误的，所以可能取到的数据是None
    if real_image_code is None:
        return jsonify(resCode='1', message="参数无效")
    # 2.2.1
    # Q:为什么要删除这个图片验证码信息？ 防止多次验证，撞库确定数据库中哪些手机号码已经被注册
    # Q：为什么是在这个位置删除？ 因为下一步就开始与数据库中的信息对比了，这是一个合理的最前面的位置
    # Q：为什么上面判断已经肯定存在了还是要用try？ 因为时间会过期（这个概率很小），还有就是网络链接你永远无法确定100%能链接成功
    try:
        redis_store.delete("image_code_{}".format(image_uuid))
    except Exception as e:
        current_app.logger.error(e)
    # 2.3 对比数据库中的图片验证码和用户发送过来的图片验证码
    if real_image_code.lower() != image_code.lower():
        return jsonify(resCode='1', message="图片验证码错误")

    # 2.4 判断手机号码是否已经存在
    try:
        user = UsersModel.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
    else:
        # db.session(UsersModel)
        if user is not None:
            # 表示手机号码已经注册了
            return jsonify(resCode='1', message="手机号码已经存在，请登录")
    # 3.业务逻辑处理 : 生成手机验证码
    # 3.1 生成6位数字的短信验证码
    sms_codes = "%06d" % (random.randint(0, 999999))
    # 3.2 保存短信验证码到redis中
    try:
        redis_store.setex("sms_codes_{}".format(mobile), 5*60, sms_codes)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(resCode='1', message="数据库保存短信验证码错误")

    # 3.3 正式发送短信验证码
    try:
        ccp = CCP()
        resp = ccp.send_message(1, mobile, [sms_codes, 5])
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(resCode='1', message="短信发送失败，第三方错误")
    else:
        # 4.返回正确结果
        if resp == 0:
            # 发送成
            return jsonify(resCode='0', message="短信发送成功！")
        else:
            return jsonify(resCode='1', message="短信发送失败，第三方错误")


