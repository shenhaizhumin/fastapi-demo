import os
import configparser
import redis
from passlib.context import CryptContext

cur_path = os.path.abspath(os.path.curdir)
print(cur_path)
# 当前文件的父路径
father_path = os.path.abspath(os.path.dirname(cur_path) + os.path.sep + ".")
print(father_path)
conf_path = os.path.join(cur_path, 'etc', 'config.ini')
print(conf_path)
# 读取配置信息
conf = configparser.ConfigParser()
conf.read(conf_path)

files_conf = dict()
for k in conf.options("file"):
    files_conf[k] = conf.get("file", k)
image_dirname = files_conf['image_dirname']
domain_name = files_conf['domain_name']

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
