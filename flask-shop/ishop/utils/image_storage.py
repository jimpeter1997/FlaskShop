# -*- coding: utf-8 -*-
# flake8: noqa
from qiniu import Auth, put_data, etag
import json
import qiniu.config



#需要填写你的 Access Key 和 Secret Key
access_key = 'amWwTHSr24xJdMek0IWy9-H7sMASrfnwifR3xJd9'
secret_key = 'JI5PvKPzsNTEziUM9KhIlLEM5Xy6wDT5o0UUjvBu'


def storage(file_data):
    """
    上传文件到七牛的方法
    :param file_data: 图片文件（二进制）
    :return:  文件在七牛云中的字符串（不包括前面的链接）
    """
    #构建鉴权对象
    q = Auth(access_key, secret_key)
    #要上传的空间
    bucket_name = 'ishop1943'
    #上传后保存的文件名
    # key = 'my-python-logo.png'
    #生成上传 Token，可以指定过期时间等
    # token = q.upload_token(bucket_name, key, 3600)
    token = q.upload_token(bucket_name, None, 3600)
    #要上传文件的本地路径
    # localfile = './sync/bbb.jpg'
    ret, info = put_data(token, None, file_data)
    # print(info)
    res = json.loads(info.text_body)
    # print(info.text_body)
    # print(res.get("hash"))
    return res.get("hash")
    # return info['key']
    # assert ret['key'] == key
    # assert ret['hash'] == etag(localfile)


if __name__ == '__main__':
    with open("./1.png", 'rb') as f:
        file_date = f.read()
        storage(file_date)