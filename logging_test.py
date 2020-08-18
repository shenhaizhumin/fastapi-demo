# -*- coding: utf-8 -*-
# import logging
# import sys
#
# # logging.basicConfig(level=logging.DEBUG)
# log = logging.getLogger('test')
# logging.basicConfig(
#     format='[%(asctime)s][pid:%(process)d][tid:%(thread)d][%(filename)s:%(lineno)d] %(levelname)s: %(message)s',
#     level=logging.DEBUG,
#     filename='test.log',
#     filemode='a',
#
#     )
# log_handler_info = logging.StreamHandler(sys.stdout)
# log_handler_err = logging.StreamHandler(sys.stderr)
# info_filter = logging.Filter()
# info_filter.filter = lambda record: record.levelno < logging.WARNING # 设置过滤等级
# err_filter = logging.Filter()
# err_filter.filter = lambda record: record.levelno >= logging.WARNING
#
# log_handler_info.addFilter(info_filter)
# log_handler_err.addFilter(err_filter)
#
# log.addHandler(log_handler_info)
# log.addHandler(log_handler_err)
#
# log.setLevel("INFO")
#
# log.debug("debug")
# log.info("info")
# log.warning("warning")
# log.error("error")

