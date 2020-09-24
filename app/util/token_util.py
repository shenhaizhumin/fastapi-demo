# coding=utf-8

import os
import uuid
import random
import base64
import hmac
from hashlib import sha1, sha256
import bcrypt
from datetime import datetime, timedelta
from app.settings import SECRET_KEY, ALGORITHM,info_logger
import jwt


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    info_logger.info(f"algorithm:{ALGORITHM},algorithm type:{type(ALGORITHM)}")
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60 * 24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt.decode('utf8')


def generate_hash_password(password: str):
    """
    :arg password
        生成hash密码
    """
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(12)).decode('utf8')


def generate_by_sha1_random():
    """ 产生一个随机的密文（消息摘要）
    :arg None
    :return 16位制的随机散列码
    """
    return sha1(os.urandom(24)).hexdigest()


def generate_by_sha1_key(key):
    """ 将一段文字生成为密文
    :arg key 要加密的一段文字
    :return 加密后的16进制的密文（散列码）
    """
    if isinstance(key, str):
        key = key.encode()
    return sha1(key).hexdigest()


def gen_uuid(type_="string"):
    """ 产生一个机器标识码
    :type_ string or int
    :return 一个基于随机数生成的16进制的机器标识码
    """
    if type_ == "string":
        return uuid.uuid4().hex
    return uuid.uuid4().int


def generate_random_string(length, type_=None):
    """
    功能： 根据不同长度生成随机字符串
    :param length: 字符串长度
    :param type_: 字符串字符类型: 数字， 字母， 所有
    :return: 具有一定长度的随机字符串 salt
    """
    if type_ == "num":
        seed = "1234567890"
    elif type_ == "abc":
        seed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    elif type_ == "word":
        seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    else:
        seed = (
            "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@$%^&*()_+=-"
        )
    string_list = list()
    for i in range(0, length):
        string_list.append(random.choice(seed))
    salt = "".join(string_list)
    return salt


def generate_base64_sign(string):
    """
    功能：将字符串进行 base64 编码加密
    :param string: 明文
    :return: 密文
    """
    if isinstance(string, str):
        return base64.b64encode(string.encode())
    return base64.b64encode(string)


def generate_sha1_sign(key, msg):
    """
    功能: 根据密钥 key，将 msg 加密产生一个 sha1 散列码，digest即包含ASCII字符
    :param key: 密钥
    :param msg: 要加密的明文
    :return: 加密后的 sha1 散列码
    """
    if isinstance(key, str):
        key_ = key + "&"
        key = key_.encode()
    if isinstance(msg, str):
        msg = msg.encode()
    hash_obj = hmac.new(key=key, msg=msg, digestmod=sha1)
    return hash_obj.digest()


def generate_sha256_sign(key, msg):
    """
    功能: 根据密钥 key，将 msg 加密产生一个 sha256 散列码
    :param key: 密钥
    :param msg: 要加密的明文
    :return: 加密后的 sha256 散列码
    """
    if isinstance(key, str):
        key = key.encode()
    if isinstance(msg, str):
        msg = msg.encode()
    hash_obj = hmac.new(key=key, msg=msg, digestmod=sha256)
    return hash_obj.hexdigest()
