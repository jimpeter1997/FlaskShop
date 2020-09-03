from werkzeug.routing import BaseConverter


# 自定义万能转换器（用正则表达式匹配）
class ReConverter(BaseConverter):
    def __init__(self, url_map, regex):
        # 调用父类的初始化方法
        super(ReConverter, self).__init__(url_map)
        # 保存正则表达式
        self.regex = regex