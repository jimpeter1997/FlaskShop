from ronglian_sms_sdk.SmsSDK import SmsSDK
import json


# accId = '容联云通讯分配的主账号ID'
accId = 'aaf98f894e52805a014e6cea68021793'
# accToken = '容联云通讯分配的主账号TOKEN'
accToken = 'ec9e6e90ef7049deb998c3414a54db19'
# appId = '容联云通讯分配的应用ID'
appId = '8aaf0708732220a60174538117bb03af'


def send_message():
    sdk = SmsSDK(accId, accToken, appId)
    # tid = '容联云通讯创建的模板'
    tid = '1'
    # mobile = '手机号1,手机号2'
    mobile = '15924239167'
    # datas = ('变量1', '变量2')
    datas = ('1943', '5')
    resp = sdk.sendMessage(tid, mobile, datas)
    print(resp)


# 单例模式: 我自己都不知道我自己是个什么类，也不知道自己会创建什么对象
class CCP(object):
    """自己封装的发送短信的辅助类"""
    instance = None  # 用来保存对象的类属性
    # def __init__(self, accId, accToken, appId):
    #     super(CCP, self).__init__(self, accId, accToken, appId)
    def __new__(cls):
        # 判断是否已经有CCP对象，如果没有就创建CCP对象，如果有的话，就直接返回CCP对象
        if cls.instance is None:
            obj = super(CCP, cls).__new__(cls)
            obj.SMSSDK = SmsSDK(accId, accToken, appId)
            cls.instance = obj
        return cls.instance

    def send_message(self, tid, mobile, datas):
        resp = self.SMSSDK.sendMessage(tid, mobile, datas)
        print(resp)
        result_status_code = json.loads(resp).get("statusCode")
        if result_status_code == '000000':
            return 0
        else:
            return 1


if __name__ == '__main__':
     ccp = CCP()
     # tid = '容联云通讯创建的模板'
     tid = '1'
     # mobile = '手机号1,手机号2'
     mobile = '15924239167'
     # datas = ('变量1', '变量2')
     datas = ('1943', '5')
     ccp.send_message(tid, mobile, datas)
     # send_message()
