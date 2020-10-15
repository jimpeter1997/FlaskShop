from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AdminUserForm(FlaskForm):
    username = StringField(
        'username',
        render_kw={'placeholder': '用户名', 'type':'text'},
        validators=[DataRequired()]
    )
    password = StringField('password', render_kw={'placeholder': '密码', 'type':'password'}, validators=[DataRequired()])
    imagenumber = StringField('imagenumber', render_kw={'placeholder': '不区分大小写', 'type':'text'}, validators=[DataRequired()])
    uuid = StringField('uuid', render_kw={'type':'hidden', 'value':''}, validators=[DataRequired()])
    submit = SubmitField('登录')
