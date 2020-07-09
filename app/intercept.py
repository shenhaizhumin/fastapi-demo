from fastapi import HTTPException, Depends, status
import jwt
from jwt import PyJWTError
from app.response import BaseError
from app.settings import SECRET_KEY, ALGORITHM, jwt_options, error_code
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.util.cache_util import Cache
from app.settings import tokenUrl
from app.models.user_info import UserInfo

validate_credentials_code = error_code

cache = Cache()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=tokenUrl)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    if 'Bearer' in token:
        token = token.split(' ')[-1]
    credentials_exception = BaseError(
        status_code=status.HTTP_401_UNAUTHORIZED,
        msg="Could not validate credentials",
        code=validate_credentials_code,
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options=jwt_options)
        username = str(payload.get("user_name"))
        uid = str(payload.get('user_id'))
        session = await cache.get_account_session(username=username, uid=uid)
        # 与本地不一致
        if not session or session != token:
            raise credentials_exception
        if username is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception

    user = UserInfo(uid, username, '')
    if user is None:
        raise credentials_exception
    return user
