import os
import configparser
import redis
from passlib.context import CryptContext
from app.util.log_util2 import get_path, get_logger
from pydantic import BaseSettings

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
profile = os.environ.get('DEPLOY_ENVIRONMENT', 'local')
if profile == 'remote':
    config_name = 'config_remote.ini'
else:
    config_name = 'config.ini'
conf_path = os.path.join(par_dir, 'config', config_name)
print("conf_path:" + conf_path)
conf_doc = configparser.ConfigParser()
conf_doc.read(conf_path)


class Settings(BaseSettings):
    LOG_DIR: str = conf_doc.get('logging', 'log_dir')
    INFO_LOGGER = get_logger(get_path(LOG_DIR, 'app_info.log'))
    ERROR_LOGGER = get_logger(get_path(LOG_DIR, 'app_error.log'))

    IMAGE_DIRNAME: str = conf_doc.get('file', 'image_dirname')
    DOMAIN_NAME: str = conf_doc.get('file', 'domain_name')
    REDIS_PORT: int = int(conf_doc.get('db.redis', 'port'))
    REDIS_HOST: str = conf_doc.get('db.redis', 'host')
    REDIS_DATABASE: int = int(conf_doc.get('db.redis', 'db'))
    # connect_pool = redis.Connection(host=REDIS_HOST, port=REDIS_PORT)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(conf_doc.get('jwt.extars', 'expire_minutes'))
    SECRET_KEY: str = conf_doc.get('jwt.extars', 'secret_key')
    ALGORITHM: str = conf_doc.get('jwt.extars', 'algorithm')
    TOKENURL: str = '/login'

    DB_URI: str = conf_doc.get('db.test', 'db_uri')
    JWT_OPTIONS: dict = {
        'verify_signature': True,
        'verify_exp': True,
        'verify_nbf': False,
        'verify_iat': True,
        'verify_aud': False
    }
    error_code: int = -200
    pwd_context = CryptContext(schemes=("bcrypt"), deprecated="auto")

    class Config:
        case_sensitive = True


setting = Settings()
