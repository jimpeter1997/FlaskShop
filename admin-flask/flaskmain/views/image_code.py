from . import admin_views
from flaskmain.libs.captcha import Captcha
from flaskmain import redis_store_for_image_code
from flask import current_app, jsonify, make_response
from io import BytesIO
import re



#@admin_views.route('/image_codes/<string:image_uuid>')
@admin_views.route('/image_codes/<re(r"[a-zA-Z0-9]{36}.png"):image>')
def get_code_image(image):
    """
    获取图片验证码链接
    :param image_uuid: 验证码编号
    :return: 正确情况下，返回验证码图片
             异常情况下，返回json数据
    """
    print("image = ", image)
    # test='kasduabshdvkjASVKDV.txt'
    # m=re.findall(r'(.+?)\.',test)
    image_uuid = re.findall(r'([a-zA-Z0-9]{36}).png',image)[0]
    text, img = Captcha.gene_code()
    # print("text = ", text)
    # 把取到text，也就是数字，保存进redis数据库
    try:
        redis_store_for_image_code.setex("image_code_{}".format(image_uuid), 5*60, text)
    except Exception as e:
        # 如果发生连接数据库错误，写入数据库
        current_app.logger.error(e)
        return jsonify(resCode='1', message="数据库错误")

    # 把取到的img发送给前端
    buf = BytesIO()
    img.save(buf, 'png')
    buf_str = buf.getvalue()

    # 返回图片
    resp = make_response(buf_str)
    resp.headers["Content-Type"] = "image/png"
    return resp

# @admin_views.route('/get_image_number/<string:image_uuid>')  # 不需要对外暴露接口，测试的时候可以开启
def get_image_number(image_uuid):
    """
    通过uuid去获取图片验证码的数值
    :param image_uuid: 前端传过来的uuid
    :return: 如果能获取到，那么返回图片验证码的数值
             如果无法获取到，那么返回None
    """
    try:
        image_number = redis_store_for_image_code.get("image_code_{}".format(image_uuid))
    except Exception as e:
        current_app.logger.error(e)
        return None

    if image_number == None:
        return None
    # 直接取出来的是二进制的数字，所以需要decode进行编码处理
    return image_number.decode()
