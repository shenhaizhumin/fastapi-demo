import os
import configparser
import redis
from passlib.context import CryptContext

# from fastapi.logger import logger
# from logging.handlers import RotatingFileHandler
import logging
from app.util.log_util import Log

formatter = logging.Formatter(
    "[%(asctime)s.%(msecs)03d] %(levelname)s [%(thread)d] - %(message)s", "%Y-%m-%d %H:%M:%S")
# handler = RotatingFileHandler('error.log', backupCount=0)
# handler.setLevel(logging.ERROR)
# logging.getLogger("fastapi")
# logger.addHandler(handler)

# handler.setFormatter(formatter)

cur_path = os.path.abspath(os.path.curdir)
print(cur_path)
# 当前文件的父路径
father_path = os.path.abspath(os.path.dirname(cur_path) + os.path.sep + ".")
print(father_path)
conf_path = os.path.join('{}/app'.format(cur_path), 'etc', 'config.ini')
print(conf_path)
# 读取配置信息
conf = configparser.ConfigParser()
conf.read(conf_path)

files_conf = dict()
for k in conf.options("file"):
    files_conf[k] = conf.get("file", k)
image_dirname = files_conf['image_dirname']
domain_name = files_conf['domain_name']

# 添加日志记录
log_conf = dict()
for k in conf.options("logging"):
    if k == "multiprocess":
        log_conf[k] = conf.getboolean("logging", k)
    else:
        log_conf[k] = conf.get("logging", k)
print(log_conf)
log_conf.update({'formatter': formatter})
log = Log(**log_conf)
logger = log.logger
# logger = LogUtil(**log_conf).logger
# logging.basicConfig(**log_conf)

"""
    redis config
"""
redis_conf = dict()
for k in conf.options("redis"):
    redis_conf[k] = conf.get("redis", k)
redis_connect = redis.Redis(**redis_conf)
"""
    jwt config
"""
jwt_conf = dict()
for k in conf.options("jwt.extars"):
    jwt_conf[k] = conf.get("jwt.extars", k)

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = jwt_conf['secret_key']
ALGORITHM = jwt_conf['algorithm']
tokenUrl = '/login'

error_code = -200

jwt_options = {
    'verify_signature': True,
    'verify_exp': True,
    'verify_nbf': False,
    'verify_iat': True,
    'verify_aud': False
}

test_db = dict()
for k in conf.options('db.test'):
    test_db[k] = conf.get('db.test', k)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
