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

f = open(image_dirname.format(filename='1.txt'))
print(f.read())
f.close()