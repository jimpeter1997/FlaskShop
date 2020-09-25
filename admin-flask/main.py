from flask import Flask, render_template, request
from forms import LonginForm
from flask_wtf import CSRFProtect



app = Flask(__name__)
app.secret_key = "ishopsecretkey!@#QEWRTY"
CSRFProtect(app)



@app.route('/')
def index():
    """
    测试函数： 整个flask是否建立完成
    :return: 字符串
    """
    return 'Hello Flask'


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    登录视图
    :return:
    """
    if request.method == 'POST':
        print("POST")
        print(type(request.form))
        print(request.form.get("login_username"))
        print(request.form.get("login_password"))
        print(request.form["login_username"])
        print(request.form["login_password"])
        print(dir(request))
        print(dir(request.form))
        print(type(request.form))
        print(dir(index))
        print(index.__doc__)
        print(index.__code__)
        pass
    form = LonginForm()
    context = {
        'title':'登录页面'
    }
    return render_template('/index/login.html', context=context, form=form)

@app.route('/logout', methods=['get'])
def logout():
    pass

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
