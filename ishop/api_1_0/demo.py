from . import api
from ishop import db, models
import logging
from flask import current_app


# 视图函数
@api.route("/", methods=['GET', 'POST'])
def index():
    logging.error('error')
    logging.warning('warning')
    logging.info('info')
    logging.debug('debug')
    current_app.logger.error('error')
    current_app.logger.warn('warn')
    current_app.logger.info('info')
    current_app.logger.debug('debug')
    return "Hello Flask"