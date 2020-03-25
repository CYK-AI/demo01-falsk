from flask import Flask
# 导入config配置信息
from config import config_map
# 导入数据库
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
# csrf防护机制
from flask_wtf import CSRFProtect
# 导入日志
import logging
from logging.handlers import RotatingFileHandler
# 导入自定义转换器
from ihome.utils.commons import ReConverter
# 导入redis
import redis


# 数据库
# 说明: 我这一上来先创建db对象，但是呢这个db对象没和app绑定到一起，什么时候绑定到一起呢，当create_app这个函数执行的
db = SQLAlchemy()
# db.init_app(app)

# 创建redis连接对象
redis_store = None

# # 相当于一个函数，可以把它理解为print()方法  之前print('caoniqq')
# # 用logging.error就会被写到日志文件中，print只是打印到屏幕，未写到日志文件中
# logging.error("caoniqq")  # 错误级别  当客户访问发生错误时，他会记录到日志文件，这样知道自己当时哪一块出现了问题
#
# # 代表警告  如果程序发生错误的话，并不影响程序的执行，而仅仅出现预期之外的结果
# logging.warn("")  # 警告级别
#
# logging.info("")  # 消息提示级别  用户每访问一条记录(不代表错误，不代表警告，只是想把这种状态保留下来的， 200码，404等)
#
# logging.debug("")  # 调试级别  专门记录调试信息


# 配置日志信息
# 设置日志的记录等级
logging.basicConfig(level=logging.WARNING)  # 调试debug级
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
# 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日记录器
logging.getLogger().addHandler(file_log_handler)


# 工厂模式
def create_app(config_name):
    """
    每次这样写创建函数说明，让别人一目了然知道各各函数和参数的用途
    创建flask的应用对象
    :param config_name: str 配置模式的名字 ('develop', 'product')
    :return:
    """
    app = Flask(__name__)

    # 根据配置模式的名字获取配置参数的类
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)

    # 上面先创建db对象，当这个函数执行的时候在把app传进来
    # 使用app初始化db
    db.init_app(app)

    # 初始化redis工具
    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)

    # 利用flask—session, 将session数据保存到redis中
    Session(app)

    # 为flask补充csrf防护
    # 他会从cookie中拿取csrf_token和body(请求体)中拿取csrf_token，这两个值需要我们自己设置
    # 前后端不分离的情况下   直接在所写的表单中填写字段csrf_token
    CSRFProtect(app)

    # 为flask添加自定义的转换器   converters['re']  re是给起的名字
    app.url_map.converters["re"] = ReConverter

    # 注册蓝图
    # 导入蓝图/ 以启动文件的目录  绝对路径
    from ihome import api_1_0
    app.register_blueprint(api_1_0.api, url_prefix="/api/v1.0")

    # 注册提供静态文件的蓝图
    from ihome import web_html
    app.register_blueprint(web_html.html)
    return app