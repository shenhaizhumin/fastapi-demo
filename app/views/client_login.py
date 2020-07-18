from fastapi import APIRouter, Depends, Form, Query
from app.intercept import get_current_user
from datetime import timedelta
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from app.schema.login_schema import PasswordRequestForm, User
from app.util.token_util import create_access_token
from app.response import BaseResponse, BaseError
from app.util.cache_util import Cache, create_user_data
from app.settings import tokenUrl
from app.models.user_info import UserInfo
from app.models import get_db, Session
from app.schema.user_schema import UserOutSchema, mobile_pattern, email_pattern
import re
from app.settings import pwd_context

login_router = APIRouter()
cache = Cache()


@login_router.post('/client/get')
async def get(x: str = Form(...)):
    return "hello world {}".format(x)


@login_router.post(tokenUrl)
async def login(schema: PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    username = schema.username
    if re.match(mobile_pattern, username):
        user = db.query(UserInfo).filter_by(mobile=username).first()
    elif re.match(email_pattern, username):
        user = db.query(UserInfo).filter_by(email=username).first()
    else:
        user = db.query(UserInfo).filter_by(username=username).first()
    if not user:
        raise BaseError(msg='Incorrect username')
    # 密码校验
    try:
        password = schema.password
        if not pwd_context.verify(password, user.password):
            return BaseError(
                msg="Incorrect password"
            )
    except Exception as e:
        raise BaseError(
            msg=f"error:{e}"
        )
    user_data = create_user_data(user.username, user.uid)
    #  设置token 过期时间
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data=user_data, expires_delta=access_token_expires)
    await cache.set_account_session(username=user.username, uid=user.uid, token=access_token)
    user.access_token = access_token
    return BaseResponse(data=UserOutSchema.from_orm(user))


@login_router.get('/client/logout')
async def logout(user=Depends(get_current_user)):
    await cache.delete_account_session(user.username, user.user_id)
    return BaseResponse()


@login_router.put('/addUser')
async def add(user: User, db: Session = Depends(get_db)):
    user_info = UserInfo()
    user_info.username = user.username
    db.add(user_info)
    db.commit()
    return BaseResponse(data=user)


@login_router.get('/allUser')
async def getAll(db: Session = Depends(get_db)):
    list = db.query(UserInfo).all()
    return BaseResponse(data=list)
