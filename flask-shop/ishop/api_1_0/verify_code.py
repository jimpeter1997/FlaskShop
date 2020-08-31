from . import api
from ishop.utils.captcha import Captcha
from ishop import redis_store
from flask import current_app,jsonify, make_response
from io import BytesIO


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
        return jsonify(errno='504', massages="保存验证码图片失败")

    buf = BytesIO()
    img.save(buf, 'png')
    buf_str = buf.getvalue()

    # 返回图片
    resp = make_response(buf_str)
    resp.headers["Content-Type"] = "image/png"
    return resp