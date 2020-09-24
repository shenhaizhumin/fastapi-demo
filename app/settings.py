import os
import configparser
import redis
from passlib.context import CryptContext
from app.util.log_util2 import get_path, get_logger

# from fastapi.logger import logger
# from logging.handlers import RotatingFileHandler
import logging

formatter = logging.Formatter(
    "[%(asctime)s.%(msecs)03d] %(levelname)s [%(thread)d] - %(message)s", "%Y-%m-%d %H:%M:%S")

# file_path = os.path.abspath(__file__)
# # project_dir = file_path[: file_path.rfind('views')]
# par_dir = os.path.dirname(file_path)
# conf_path = os.path.join(par_dir, 'etc', 'config.ini')
# print(conf_path)
#
# # 读取配置信息
# conf = configparser.ConfigParser()
# conf.read(conf_path)
#
# info_logger = get_logger(get_path('./logs', 'app_info.log'))
# error_logger = get_logger(get_path('./logs', 'app_error.log'))
#
# files_conf = dict()
# for k in conf.options("file"):
#     files_conf[k] = conf.get("file", k)
# image_dirname = files_conf['image_dirname']
# domain_name = files_conf['domain_name']
#
# """
#     redis config
# """
# redis_conf = dict()
# for k in conf.options("redis"):
#     redis_conf[k] = conf.get("redis", k)
# redis_connect = redis.Redis(**redis_conf)
# """
#     jwt config
# """
# jwt_conf = dict()
# for k in conf.options("jwt.extars"):
#     jwt_conf[k] = conf.get("jwt.extars", k)
#
# ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
# SECRET_KEY = jwt_conf['secret_key']
# ALGORITHM = jwt_conf['algorithm']
# tokenUrl = '/login'
#
# error_code = -200
#
# jwt_options = {
#     'verify_signature': True,
#     'verify_exp': True,
#     'verify_nbf': False,
#     'verify_iat': True,
#     'verify_aud': False
# }
#
# test_db = dict()
# for k in conf.options('db.test'):
#     test_db[k] = conf.get('db.test', k)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

import re
import yaml

path_matcher = re.compile(r'.*\$\{([^}^{]+)\}.*')


def path_constructor(loader, node):
    return os.path.expandvars(node.value)


class EnvVarLoader(yaml.SafeLoader):
    pass


EnvVarLoader.add_implicit_resolver('!path', path_matcher, None)
EnvVarLoader.add_constructor('!path', path_constructor)

# _env = os.environ.get('CFG_ENV')
_config_path = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)) + 'configs.yml'
conf_doc = yaml.load(open(_config_path), Loader=EnvVarLoader)
# conf = conf_doc[_env]

log_dir = conf_doc['logging']['log_dir']
info_logger = get_logger(get_path(log_dir, 'app_info.log'))
error_logger = get_logger(get_path(log_dir, 'app_error.log'))

image_dirname = conf_doc['file']['image_dirname']
domain_name = conf_doc['file']['domain_name']

redis_port = int(conf_doc['db.redis']['port'])
redis_host = conf_doc['db.redis']['host']
redis_database = int(conf_doc['db.redis']['db'])
redis_connect = redis.Redis(host=redis_host, port=redis_port, db=redis_database)

ACCESS_TOKEN_EXPIRE_MINUTES = int(conf_doc['jwt.extars']['expire_minutes'])
SECRET_KEY = conf_doc['jwt.extars']['secret_key']
ALGORITHM = conf_doc['jwt.extars']['algorithm']
tokenUrl = '/login'

db_uri = conf_doc['db.test']['db_uri']
jwt_options = {
    'verify_signature': True,
    'verify_exp': True,
    'verify_nbf': False,
    'verify_iat': True,
    'verify_aud': False
}
error_code = -200
