from . import api
from ihome import db
import logging
# flask封装的全局上下文 current_app
from flask import current_app


@api.route('/index')
def index():
    current_app.logger.error("error msg")
    current_app.logger.warn("warn msg")
    current_app.logger.info("info msg")
    current_app.logger.debug("debug msg")
    return 'index page'