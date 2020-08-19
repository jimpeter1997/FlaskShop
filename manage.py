"""
单一文件下的情况，我们的目标是把单一的文件拆分成一个项目文件夹

"""
from ishop import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


# 创建flask应用对象
app = create_app("develop")

manager = Manager(app)
Migrate(app, db)
manager.add_command("db", MigrateCommand)

# 启动入口
if __name__ == '__main__':
    manager.run()