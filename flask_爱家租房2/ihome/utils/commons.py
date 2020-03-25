"""
    存放通用的主件信息

    定义一个正则转换器
    首先要以类的方式去定义  继承自一个父类  from werkzeug.routing import BaseConverter
"""

from werkzeug.routing import BaseConverter


# 定义一个正则转换器
class ReConverter(BaseConverter):
    # url_map 固定的    regex  传送过来的正则表达式
    def __init__(self, url_map, regex):
        # 调用父类的初始化方法
        super(ReConverter, self).__init__(url_map)
        # 保存正则表达式
        self.regex = regex











