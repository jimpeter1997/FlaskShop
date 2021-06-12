# 绑定app与SQLAlchmey实例，同时为项目添加脚本工具
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flaskmain import create_app, db


# 创建flask应用对象
app = create_app('develop')

manager = Manager(app)
Migrate(app, db)
manager.add_command("db", MigrateCommand)

# 启动入口
if __name__ == '__main__':
    manager.run()


# from flaskmain import create_app, db
# from flask_migrate import Migrate, MigrateCommand
# from flask_script import Manager
#
#
# app = create_app()
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)
# Migrate(app, db)
#
# if __name__ == '__main__':
#     manager,run()
