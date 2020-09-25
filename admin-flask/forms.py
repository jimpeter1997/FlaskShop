from flask_wtf import FlaskForm  # 导入表单基类
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class LonginForm(FlaskForm):
    login_username = StringField("用户名", validators=[DataRequired("用户名不能为空")])
    login_password = StringField("密码", validators=[DataRequired("密码不能为空")])
    # login_recaptcha = RecaptchaField()  # 国内无法使用
    login_submit = SubmitField("点击登录")