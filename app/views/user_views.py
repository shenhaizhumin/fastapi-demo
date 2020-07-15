from fastapi import APIRouter, Depends, Request
from app.intercept import get_current_user
from app.models.user_info import UserInfo
from app.response import BaseResponse, BaseError
from app.models import Session, get_db
from app.schema.user_schema import UserUpdateSchema, UserInSchema, UserOutSchema
from app.util import token_util
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from app.util.cache_util import Cache
from datetime import datetime, timedelta

user_router = APIRouter()
cache = Cache()


@user_router.post('/register')
async def register(req: Request, schema: UserInSchema, db: Session = Depends(get_db)):
    if not any([schema.username, schema.mobile, schema.email]):
        raise BaseError(msg='用户名/手机号/邮箱 必须填写其中一个.')
    if not schema.password:
        raise BaseError(msg='missing password')
    if schema.username and db.query(UserInfo).filter_by(username=schema.username).one_or_none():
        raise BaseError(msg='username already exists')
    if schema.mobile and db.query(UserInfo).filter_by(mobile=schema.mobile).one_or_none():
        raise BaseError(msg='mobile already exists')
    if schema.email and db.query(UserInfo).filter_by(email=schema.email).one_or_none():
        raise BaseError(msg='email already exists')
    schema.latest_ip = req.client.host
    # 生成密码串
    pwd = token_util.generate_hash_password(schema.password)
    schema.password = pwd
    user = UserInfo.create(db, **schema.__dict__)
    # 设置token
    user_data = {
        'username': user.username,
        'uid': user.uid
    }
    access_token = token_util.create_access_token(data=user_data, expires_delta=timedelta(ACCESS_TOKEN_EXPIRE_MINUTES))
    await cache.set_account_session(user.username, user.uid, access_token)
    user.access_token = access_token
    # 更新登录时间
    user.update(db, latest_time=datetime.now())
    return BaseResponse(data=UserOutSchema.from_orm(user))


@user_router.get('/userInfo')
async def user_info(user: UserInfo = Depends(get_current_user)):
    return BaseResponse(data=UserOutSchema.from_orm(user))


@user_router.put('/updateUser')
async def update_user(schema: UserUpdateSchema, current_user: UserInfo = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    update_info = {}
    if schema.nickname:
        update_info.update({'nickname': schema.nickname})
    if schema.avatar_url:
        update_info.update({'avatar_url': schema.avatar_url})
    if schema.password:
        update_info.update({'password': schema.password})
    user = current_user.update(db=db, **update_info)
    return BaseResponse(data=UserOutSchema.from_orm(user))
