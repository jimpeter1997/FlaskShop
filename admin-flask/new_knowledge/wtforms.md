# flask-wtf


## 快速入门


```python
# 将代码放入forms.py中
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired



class MyForm(FlaskForm):
    name = StrgingField('name', validators=[DataRequired()])

```

```python
# python中使用
from myapp.forms import MyForm
from flask import render_template

...


@app.route('/')
def index():
    return render_template('index.html', form=Myform())
```

```html
<!-- 模板中渲染 -->

<form method="post" action='/'>
    {{ form.csrf_token }}
    {{ form.name.lable }} {{ from.name(size=20) }}
    <input type="submit" name="" value="提交">
</form>
```

```python
@app.route('/', methods=['GET', 'POST'])
def index():
    form = Myform()
    if form.calidate_on_submit():
        return "验证通过"
    return render_template('index.html', form=form)

你不需要把 request.form 传给 Flask-WTF；
Flask-WTF 会自动加载
便捷的方法 validate_on_submit() 将会检查是否是一个 POST 请求并且请求是否有效。

```


## form的属性和方法

### 属性
- data： 返回一个包含表单数据的字典，获取莫个字段：form.字段名.data，如上例：from.name.data
- errors: 返回一个包含每个字段错误信息的字典，必须先执行form.calidate()验证后才会生成，未验证或者没有错误则返回空字典
- meta: 用于使用元类

### 方法

- validate(): 验证数据是否通过
- populate_obj(obj): 用与表单的数据修改某实例的属性，比如一个修改user资料的例子：
```python
def edit_profile(request):
    user = User.objects.get(pk=request.session['userid'])
    from = EditProfileForm(request.POST, obj=user)

    if request.POST and form.validate():
        from.populate_obj(user)
        user.save()
        return redirect('/home')

    return render_to_response('edit_profile.html', form=form)
```

## 字段验证器

我们可以通过创建名为 validate_ + 字段名 的函数来自定义某个字段的验证。

```python

class SinnupForm(FlaskForm):
    age = IntegerField('age')

    def validate_age(form, field):
        if field.data < 13:
            raiase ValidateionError("")


```

## wtforms 字段类型

- BooleanField ： 生成 <input type =“checkbox”>，使用 default = "checked" 会将默认选项设置为 True。
- DateField ： 对应datetime.date的数据类型
- DateTimeField： 对应datetime.datetime的数据类型
- DecimalField: 处理带小数的数字类型
- FileField ： 处理文件类型
- MultipleFileField： 处理多个文件的类型
- FloatField： 浮点数类型
- IntegerField: 整数类型
- RadioField : 前端渲染成选项类型（radio）

```python
# 后端定义
sex = RadioField(
        label  = 'sex',
        choices = [('male','男'), ('female','女')]
        )

# 前端渲染
{% for subfield in form.work %}
    <tr>
        <td>{{ subfield }}</td>
        <td>{{ subfield.label }}</td>
    </tr>
{% endfor %}

```

- SelectField
- SelectMultipleField
- SubmitField
- StringField
- HiddenField
- PasswordField
- TextAreaField



## wtforms 字段参数

- label: 字段名称
- validators : 字段要用的验证器
- filters: 字段要用到的过滤器
- description: 字段的描述，通常用于帮助文本
- id： 在前端渲染表单生成的id
- default： 前端渲染表单时生成的input的默认值
- widgets： 窗口小部件，改变字段在前端表单的渲染形式，例如某个字段享用TextArea形式：

```python
from wtforms.widgets import TextArea


class MyForm(FlaskForm):
    name = StringField(label='名字', widget=TextArea())
```

- render_kw: 参数格式为字典，在前端渲染你表单时，提供额外的属性，比如某个input我想设定“placeholder="姓名"”
```python
class MyForm(FlaskForm):
    name = StringField(label="name", render_kw={'placeholder':"姓名"})
```

## 内置验证器

- DataRequired: 数据必须填写
- Email
- EqualTo： 检验两个字段是否相等，一个验证两次密码输入是否一致

```python
class MyForm(FlaskForm):
    password1 = StringField(
        label = "密码",
        validators = [
            InputRequired(message="请输入密码"),
            EqualTo('password2', message="两次密码输入不一致")
        ]
    )
    password2 = StringField(
        label = "再次输入密码",
        validators = [InputRequired(message="请输入密码")]
    )
```

- InputRequired
- IPAddress
- Length : 参数：min、max表示最小和最大长度; message表示错误信息
- MacAddress
- NumberRange ： 验证数值的最大和最小值，整数、浮点数都有效;参数：min、max和message
- Optional ： 使用后允许空输入
- Regexp ： 正则表达式
- URL
- UUID
- AnyOf ： 把输入数据和某个之比较（输入的数据必须为某值）
- NoneOf ： 把输入数据和某个值比较（输入的数据不能为某值）

## 自定义验证器

- 自定义一个验证器，检验name字段的输入长度

```python
class MyForm(FlaskForm):
    name = StringField("name", [InputRequired()])

    def validate_name(from, field):
        if len(field.data) > 50:
            raise ValidationError("Name must be less than 50 characters !")
```

- 单独用一个函数作为验证器，这样验证器就能重复使用

```python
def my_length_check(form, field):
    if len(field.data) > 50:
        raise ValidationError("Field must be less than 50 characters ! ")

class MyForm(FlaskForm):
    name = StringField("name", [InputRequired(), my_length_check])
```

- 编写更复杂的验证器， 比如带参数的验证器

```python
def length(min=-1, max=-1):
    messsage = "Must be between %d and %d characters long. " % (min, max)

    def _length(form, field):
        l = field.data and len(field.data) or 0
        if l < min or max != -1 and l > max:
            raise ValidationError(message)

    return _length
```

- 为了更好代码重用，可以包装成类：
```python
class Length(object):
    def __init__(self, min=1, max=-1, message=None):
        self.min = min
        self.max = max
        if not message:
            message = 'Field must be between {} and {} characters long.'.format(min, max)

        self.message = message

    def __call__(self, form, field):
        l = field.data and len(field.data) or 0
        if l < self.min or self.max != -1 and l > self.max:
            raise ValidatrionError(self.message)


length = Length(min=1, max=5)


class MyForm(FlaskForm):
    work = StringField(
        label = 'work',
        validators = [
            InputRequired(),
            length
        ]
    )
```
