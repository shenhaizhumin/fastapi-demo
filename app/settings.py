import os
import configparser
import redis
from passlib.context import CryptContext
from app.util.log_util2 import get_path, get_logger

# from fastapi.logger import logger
# from logging.handlers import RotatingFileHandler
import logging

formatter = logging.Formatter(
    "(%(asctime)s.%(msecs)03d) %(levelname)s (%(thread)d) - %(message)s", "%Y-%m-%d %H:%M:%S")

# import re
# import yaml
#
# path_matcher = re.compile(r'.*\$\{((^}^{)+)\}.*')
#
#
# def path_constructor(loader, node):
#     return os.path.expandvars(node.value)
#
#
# class EnvVarLoader(yaml.SafeLoader):
#     pass
#
#
# EnvVarLoader.add_implicit_resolver('!path', path_matcher, None)
# EnvVarLoader.add_constructor('!path', path_constructor)
#
# # _env = os.environ.get('CFG_ENV')
# _config_path = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)) + 'configs.yml'
# conf_doc = yaml.load(open(_config_path), Loader=EnvVarLoader)
# conf = conf_doc.get(_env)

# 读取配置信息
file_path = os.path.abspath(__file__)
par_dir = os.path.dirname(file_path)
conf_path = os.path.join(par_dir, 'etc', 'config.ini')
conf_doc = configparser.ConfigParser()
conf_doc.read(conf_path)

from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        case_sensitive = True

    LOG_DIR = conf_doc.get('logging', 'log_dir')
    INFO_LOGGER = get_logger(get_path(LOG_DIR, 'app_info.log'))
    ERROR_LOGGER = get_logger(get_path(LOG_DIR, 'app_error.log'))

    IMAGE_DIRNAME = conf_doc.get('file', 'image_dirname')
    DOMAIN_NAME = conf_doc.get('file', 'domain_name')
    REDIS_PORT = int(conf_doc.get('db.redis', 'port'))
    REDIS_HOST = conf_doc.get('db.redis', 'host')
    REDIS_DATABASE = int(conf_doc.get('db.redis', 'db'))
    REDIS_CONNECT = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DATABASE)
    ACCESS_TOKEN_EXPIRE_MINUTES = int(conf_doc.get('jwt.extars', 'expire_minutes'))
    SECRET_KEY = conf_doc.get('jwt.extars', 'secret_key')
    ALGORITHM = conf_doc.get('jwt.extars', 'algorithm')
    TOKENURL = '/login'

    DB_URI = conf_doc.get('db.test', 'db_uri')
    JWT_OPTIONS = {
        'verify_signature': True,
        'verify_exp': True,
        'verify_nbf': False,
        'verify_iat': True,
        'verify_aud': False
    }
    error_code = -200
    pwd_context = CryptContext(schemes=("bcrypt"), deprecated="auto")


setting = Settings
