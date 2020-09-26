##  建立了一个一般常用flask工程目录

### 使用了如下的模块
- flask： 不解释了
- redis： 连接redis数据库，用于保存session
- pymysql： 作为连接mysql数据库的驱动
- flask-wtf： 处理表单问题，提供csrf_token的保护
- flask-sqlalchemy： 把数据库作为模型类来使用
- flask-session： 将flask的session保存到服务端(redis)来
- flask-script: 为flask提供脚本服务（可以像django的方式来启动flask）
- flask-migrate： 为flask提供数据库建立、迁移、修改等
- logger(这个库是python3自带的，其他都需要安装): 提供日志文件 

### 文件夹的作用，请查看各自文件夹内的readme