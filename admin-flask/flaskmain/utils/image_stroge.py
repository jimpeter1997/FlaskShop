from qiniu import Auth, put_file, etag
import qiniu.config


#需要填写你的 Access Key 和 Secret Key
access_key = 'amWwTHSr24xJdMek0IWy9-H7sMASrfnwifR3xJd9'
secret_key = 'JI5PvKPzsNTEziUM9KhIlLEM5Xy6wDT5o0UUjvBu'

#构建鉴权对象
q = Auth(access_key, secret_key)

#要上传的空间
bucket_name = 'ishop002'

#上传后保存的文件名
#key = '1.png'
key = None

#生成上传 Token，可以指定过期时间等
token = q.upload_token(bucket_name, key, 3600)

#要上传文件的本地路径
localfile = './123.png'
ret, info = put_file(token, key, localfile)
print(info)
print(ret)
# assert ret['key'] == key
# assert ret['hash'] == etag(localfile)
#
# def upload_image():
