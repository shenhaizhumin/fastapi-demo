from fastapi import APIRouter, Depends, Form, Query
from app.intercept import get_current_user
from datetime import timedelta
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from app.schema.login_schema import PasswordRequestForm, User
from app.util.token_util import create_access_token
from app.response import BaseResponse, BaseError
from app.util.cache_util import Cache
from app.settings import tokenUrl
from app.models.user_info import user_info
from app.database import get_db
from sqlalchemy.orm import Session

login_router = APIRouter()
cache = Cache()


@login_router.post('/client/get')
async def get(x: str = Form(...)):
    return "hello world {}".format(x)


@login_router.post(tokenUrl)
# async def login(username: str = Form(...), password: str = Form(...)):
async def login(schema: PasswordRequestForm = Depends()):
    user_id = 1
    username = schema.username
    #  设置token 过期时间
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    user_data = {
        'user_id': user_id, 'user_name': username
    }
    access_token = create_access_token(data=user_data, expires_delta=access_token_expires)
    await cache.set_account_session(username=username, uid=str(user_id), token=access_token)
    return BaseResponse(data={
        'id': user_id,
        'account_username': username,
        'access_token': access_token
    })


@login_router.get('/client/logout')
async def logout(user=Depends(get_current_user)):
    await cache.delete_account_session(user.username, user.user_id)
    return BaseResponse()


@login_router.put('/addUser')
async def add(user: User, db: Session = Depends(get_db)):
    userInfo = user_info()
    userInfo.username = user.username
    db.add(userInfo)
    db.commit()
    return BaseResponse(data=user)


@login_router.get('/allUser')
async def getAll(db: Session = Depends(get_db)):
    list = db.query(user_info).all()
    return BaseResponse(data=list)
