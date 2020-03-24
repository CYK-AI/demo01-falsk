from ihome import create_app, db
# 导入flask脚本
from flask_script import Manager
# Migrate迁移的执行者， MigarteCommand命令解析人员
from flask_migrate import Migrate, MigrateCommand

# 创建flask的应用对象
app = create_app('develop')

manager = Manager(app)
# 将迁移者保存到app中，再次用到的时候还会用到数据库
Migrate(app, db)
# 添加命令
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()
