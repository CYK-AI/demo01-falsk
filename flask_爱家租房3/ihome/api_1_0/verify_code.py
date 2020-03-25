from . import api
from ihome.utils.captcha.captcha import captcha
# 导入redis实例   导入设置好的redis有效期
from ihome import redis_store, constants
# 记录日志
from flask import current_app, jsonify, make_response
# 导入错误码状态信息
from ihome.utils.response_code import RET

# 127.0.0.1:5000/api/v1.0/image_codes/图片验证码的编号<image_code_id>

# 定义视图
@api.route('/image_codes/<image_code_id>')
def get_image_code(image_code_id):
    """
    获取图片验证码
    :param: image_code_id   图片验证码的编号
    :return: 正常情况下：验证码图片  错误情况下: 返回json
    """
    # 四步走
    # 1、获取参数  已经在函数中获取， 所以这一步省略
    # 2、检验参数  已经完成 <image_code_id>  如果不在上面传参数，那么这个视图函数进不来

    # 3、业务逻辑处理
    # 生成验证码图片
    # 名字  真实文本， 图片数据
    name, text, image_data = captcha.generate_captcha()
    # 将验证码真实值与编号保存到redis中
    # redis中的数据类型 字符串 列表 哈希 set
    # Redis数据库是键值对的形式 "key": xxxx
    # 我们还要设置有效期
    # 使用哈希维护有效期的时候只能整体设置，不是很方便， 一条过期，整体删除
    # "image_codes": {"id1": "abc", "id2": "def", "": ""} 哈希 hset("image_codes", "id1": "abc") hget("image_codes","id1")
    # 单条维护记录， 选用字符串类型
    # "image_code_编号1": "真实值"
    # "image_code_编号2": "真实值"

    # # 单条记录进行维护
    # redis_store.set("image_code_%s" % image_code_id, text)
    # # 设置有效期
    # redis_store.expire("image_code_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES)

    # 上面两步骤可以合到一步
    # 现在redis和代码两台机器，有可能出现断网情况，这时我们需要捕获异常
    try:
        #                 记录名字                               有效期                        记录值
        redis_store.setex("image_code_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        # 将错误信息记录日志
        current_app.logger.error(e)
        # return jsonify(errno=RET.DBERR, errmsg="save image code failed")
        return jsonify(errno=RET.DBERR, errmsg="保存图片验证码信息失败")

    # 返回图片
    resp = make_response(image_data)
    resp.headers["Content-Type"] = "image/jpg"
    return resp
    # 如果没有像上面设置
    # Content-TypeError  "text/html"  返回的文本文件 所以我们设置一下
    # 4、返回值