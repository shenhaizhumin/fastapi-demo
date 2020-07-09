from app.settings import redis_connect


class Cache:
    @classmethod
    async def get_account_session(cls, username: str, uid: str):
        key = get_token_key(username, uid)
        value = redis_connect.get(key)
        if not value:
            return None
        return value.decode()

    @classmethod
    async def set_account_session(cls, username: str, uid: str, token: str):
        key = get_token_key(username, uid)
        return redis_connect.set(key, token)

    @classmethod
    async def delete_account_session(cls, username: str, uid: str):
        redis_connect.delete(get_token_key(username, uid))


def get_token_key(username: str, uid: str):
    return '{}_{}'.format(username, uid)
