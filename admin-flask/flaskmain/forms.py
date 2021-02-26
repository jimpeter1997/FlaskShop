from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, NumberRange
import datetime


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
    company_name = StringField('company_name', redner_kw={'type':'text'}, validators=[DataRequired(message='不能为空')])
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



class SelfIntegerField(IntegerField):
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = int(valuelist[0])
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('输入必须是一个有效的数字！'))


class SelfDateTimeField(DateTimeField):
    def process_formdata(self, valuelist):
        if valuelist:
            date_str = ' '.join(valuelist)
            try:
                self.data = datetime.datetime.strptime(date_str, self.format)
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('输入的并不是一个符合格式的时间'))


# 过滤特殊字符
class SelfStringField(StringField):
    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist[0]
        elif self.data is None:
            self.data = ''


# 活动表单
class ActivityForm(FlaskForm):
    activity_name = StringField(label="活动名称", id='activity_name', render_kw={'type':'text'}, validators=[DataRequired(message="不能为空")])
    desc = StringField(label="活动描述", id='desc', render_kw={'type':'text'}, validators=[DataRequired(message="不能为空")])
    off_percent = SelfIntegerField(label="折扣力度(%)", id='off_percent', validators=[NumberRange(min=0,max=99, message="打折必须在0到99之间的数字")])
    package_time = SelfDateTimeField(label="发货时间", id='package_time', render_kw={'type':'text'})
    start_time = SelfDateTimeField(label="开始时间",id='start_time', render_kw={'type':'text'})
    close_time = SelfDateTimeField(label="结束时间", id='close_time', render_kw={'type':'text'})
    is_active = BooleanField(label="是否激活", id='is_active', validators=[DataRequired(message="不能为空")])
    count = SelfIntegerField(label="活动数量", id='count')
    submit = SubmitField('提交')
