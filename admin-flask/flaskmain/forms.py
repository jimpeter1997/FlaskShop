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


class CompanyForm(FlaskForm):
    # 公司基础信息
    company_name = StringField('company_name', redner_kw={'type':'text'}, validators=[DataRequired()])
    web_title = StringField('web_title', redner_kw={'type':'text'}, validators=[DataRequired()])
    web_key_wrods = StringField('web_key_wrods', redner_kw={'type':'text'}, validators=[DataRequired()])
    web_description = StringField('web_description', redner_kw={'type':'text'}, validators=[DataRequired()])
    web_copyright = StringField('web_copyright', redner_kw={'type':'text'}, validators=[DataRequired()])
    # 容联云短信发送
    ronglianyun_accId = StringField('ronglianyun_accId', redner_kw={'type':'text'}, validators=[DataRequired()])
    ronglianyun_accToken = StringField('ronglianyun_accToken', redner_kw={'type':'text'}, validators=[DataRequired()])
    ronglianyun_appId = StringField('ronglianyun_appId', redner_kw={'type':'text'}, validators=[DataRequired()])
    # 七牛云图床信息
    qiniu_acess_key = StringField('qiniu_acess_key', redner_kw={'type':'text'}, validators=[DataRequired()])
    qiniu_secret_key = StringField('qiniu_secret_key', redner_kw={'type':'text'}, validators=[DataRequired()])

    submit = SubmitField('保存修改')