# 导入蓝图  导入flask封装的全局上下文
from flask import Blueprint, current_app, make_response
# 导入可以生成的csrf_token
from flask_wtf import csrf


# 提供静态文件的蓝图
html = Blueprint("web_html", __name__)


# 127.0.0.1:5000/()
# 127.0.0.1:5000/(index.html)
# 127.0.0.1:5000/(register.html)  后面路由作为整体部分
# 127.0.0.1:5000/favicon.ico 浏览器认为的网站标识  浏览器会自己请求这个资源

@html.route("/<re(r'.*'):html_file_name>")  # int float str path
def get_html(html_file_name):
    """
    提供html文件
    :param file_name:  我们定义的提起参数的名字
    :return:
    """

    # 进行判断 是否为空或者有其他文件# 127.0.0.1:5000/()  127.0.0.1:5000/(index.html)
    # 如果html_file_name为 "空字符串" 则访问的路径/，请求的是主页
    if not html_file_name:
        html_file_name = "index.html"
    # 如果资源名不是favicon.ico
    if html_file_name != "favicon.ico":
        html_file_name = "html/" + html_file_name

    # 创建一个csrf_token的值
    # 通过这个generate_csrf()函数就能给我们生成csrf_token的值
    csrf_token = csrf.generate_csrf()  # 一调用就会生成一个值

    # 在全局的app当中会有一个send_static_file专门让我们返回静态文件的
    # flask提供的返回静态文件的方法
    # return current_app.send_static_file(html_file_name)
    # 上面是原来的，没有将csrf_token提前放入的cookie

    # 以下将csrf_token提前放入
    # 先构建响应对象，通过make_response()方法，进行处理，形成response对象
    resp = make_response(current_app.send_static_file(html_file_name))

    # 设置cookie值  我们不用设置有效期，因为默认的就是本次浏览器打开生效，关闭之后失效，临时有效
    resp.set_cookie('csrf_token', csrf_token)
    return resp