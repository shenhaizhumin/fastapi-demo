from app.settings import setting, conf_path
import redis

print("conf_path:" + conf_path)
REDIS_CONNECT = redis.Redis(host=setting.REDIS_HOST, port=setting.REDIS_PORT, db=setting.REDIS_DATABASE)
print(f"keys *:{REDIS_CONNECT.keys('*')}")


class Cache:
    @classmethod
    async def get_account_session(cls, username: str, uid: str):
        key = get_token_key(username, uid)
        value = REDIS_CONNECT.get(key)
        if not value:
            return None
        return value.decode()

    @classmethod
    async def set_account_session(cls, username: str, uid: str, token: str):
        key = get_token_key(username, uid)
        return REDIS_CONNECT.set(key, token)

    @classmethod
    async def delete_account_session(cls, username: str, uid: str):
        REDIS_CONNECT.delete(get_token_key(username, uid))


def get_token_key(username: str, uid: str):
    return '{}_{}'.format(username, uid)


def create_user_data(username: str, uid: str):
    return {
        'username': username,
        'uid': uid
    }
