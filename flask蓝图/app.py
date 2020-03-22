from flask import Flask
from admin import admin
from user import user

app = Flask(__name__)


# 参数url_prefix='/xxx'的意思是设置request.url中的url前缀，
# 即当request.url是以/admin或者/user的情况下才会通过注册的蓝图的视图方法处理请求并返回
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(user, url_prefix='/user')



@app.route('/')
def index():
    return 'index'


@app.route('/list')
def list():
    return 'list'


@app.route('/detail')
def detail():
    return 'detail'


if __name__=='__main__':
    app.run()
