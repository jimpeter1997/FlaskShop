from . import api


# 视图函数
@api.route("/", methods=['GET', 'POST'])
def index():
    return "Hello Flask"