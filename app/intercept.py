from fastapi import HTTPException, Depends, status
import jwt
from jwt import PyJWTError
from app.response import BaseError
from app.settings import setting
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.util.cache_util import Cache
from app.models.user_info import UserInfo
from app.models import get_db

validate_credentials_code = setting.error_code

cache = Cache()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=setting.TOKENURL)


async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    if 'Bearer' in token:
        token = token.split(' ')[-1]
    credentials_exception = BaseError(
        status_code=status.HTTP_401_UNAUTHORIZED,
        msg="Could not validate credentials",
        code=validate_credentials_code,
    )
    try:
        payload = jwt.decode(token, setting.SECRET_KEY, algorithms=[setting.ALGORITHM], options=setting.JWT_OPTIONS)
        username = str(payload.get("username"))
        uid = str(payload.get('uid'))
        session = await cache.get_account_session(username=username, uid=uid)
        # 与本地不一致
        if not session or session != token:
            raise credentials_exception
        if username is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    user = db.query(UserInfo).filter_by(username=username).first()
    if user is None:
        raise credentials_exception
    if not user.enable:
        raise BaseError(msg='该用户已被禁用')
    return user
