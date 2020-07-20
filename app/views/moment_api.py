from fastapi import APIRouter, Depends, Query, Path
from app.models import Session, get_db
from app.models.user_info import UserInfo
from app.models.moment import Moment, Collect, Comment
from app.intercept import get_current_user
from app.response import BaseError, BaseResponse
from app.schema.moment_schema import CollectInSchema, MomentInSchema, CommentInSchema, MomentOutSchema, \
    CommentOutSchema, CollectOutSchema, MomentByDaySchema,UserSchema
from app.models.file_entity import FileEntity
from app.util.date_util import released_time
import datetime
from typing import List

moment_router = APIRouter()


@moment_router.get('/moments')
async def get_moments(current_user: UserInfo = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    '''
    查询当前用户的朋友圈列表
    :return:
    '''
    # if user_id:
    #     if not db.query(UserInfo).filter_by(id=user_id).first():
    #         raise BaseError('查询的用户已不存在！')
    #     moments = db.query(Moment).filter_by(user_id=user_id).order_by(Moment.publish_time.desc()).all()
    # else:
    #     moments = db.query(Moment).order_by(Moment.publish_time.desc()).all()
    moments = db.query(Moment).order_by(Moment.publish_time.desc()).all()
    results = []
    for m in moments:
        m.release_time = released_time(m.publish_time)
        results.append(MomentOutSchema.from_orm(m))
    # results = [MomentOutSchema.from_orm(m) for m in moments]
    return BaseResponse(data=results)


@moment_router.get('/moments/{user_id}')
async def get_moments(user_id: int = Path(...),
                      db: Session = Depends(get_db), current_user: UserInfo = Depends(get_current_user)):
    '''
    查询用户的朋友圈列表
    :return:
    '''
    user = db.query(UserInfo).filter_by(id=user_id).first()
    if not user:
        raise BaseError('查询的用户已不存在！')
    moments = db.query(Moment).filter_by(user_id=user_id).order_by(Moment.publish_time.desc()).all()
    results = {

    }
    today = datetime.datetime.today()
    yesterday = today - datetime.timedelta(days=1)
    current_year = datetime.datetime.now().year
    for m in moments:
        publish_time = m.publish_time
        m.release_time = released_time(publish_time)
        current_date = publish_time.date()
        if current_date == today.date():
            method(results, '今天', m)
        elif current_date == yesterday.date():
            method(results, '昨天', m)
        else:
            if current_year == current_date.year:
                key = current_date.strftime('%m-%d')
                method(results, key, m)
            else:
                key = current_date.strftime('%Y-%m-%d')
                method(results, key, m)
    res = []
    for k in results.keys():
        data = MomentByDaySchema(day_key=k, moments=results[k])
        res.append(data)
    return BaseResponse(data={
        'list': res,
        'friendInfo': UserSchema.from_orm(user)
    })


def method(results: dict, key: str, m: Moment):
    if results.get(key):
        results[key].append(MomentOutSchema.from_orm(m))
    else:
        results[key] = [MomentOutSchema.from_orm(m)]


@moment_router.post('/moments/publish')
async def publish_moment(schema: MomentInSchema, current_user: UserInfo = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    '''
        发布动态
    :param schema:
    :param current_user:
    :param db:
    :return:
    '''
    user_id = current_user.id
    moment = Moment(
        user_id=user_id,
        content=schema.content,
        content_url=schema.content_url,
        publish_time=datetime.datetime.now()
    )
    db.add(moment)
    # 拿到moment_id
    db.commit()
    image_ids = schema.images
    # 绑定图片列表
    if image_ids and len(image_ids) > 0:
        for i in image_ids:
            file_entity = db.query(FileEntity).filter_by(id=i.id).first()
            if file_entity:
                file_entity.moment_id = moment.id
    db.commit()
    return BaseResponse(data=MomentOutSchema.from_orm(moment))


@moment_router.post('/moments/publishComment')
async def publish_comment(schema: CommentInSchema, current_user: UserInfo = Depends(get_current_user),
                          db: Session = Depends(get_db)):
    '''
    发布 评论
    :param schema:
    :param current_user:
    :param db:
    :return:
    '''
    moment_id = schema.moment_id
    if not db.query(Moment).filter_by(id=moment_id).first():
        raise BaseError(msg='moment not exists')
    user_id = current_user.id
    user_name = current_user.nickname
    comment = Comment(
        operator_user_id=user_id,
        content=schema.content,
        moment_id=moment_id,
        publish_time=datetime.datetime.now()
    )
    db.add(comment)
    db.commit()
    db.flush()
    return BaseResponse(data=CommentOutSchema.from_orm(comment))


@moment_router.post('/moments/collect')
async def collect_moment(schema: CollectInSchema, current_user: UserInfo = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    '''
    收藏
    :param schema:
    :param current_user:
    :param db:
    :return:
    '''
    moment_id = schema.moment_id
    if not db.query(Moment).filter_by(id=moment_id).first():
        raise BaseError(msg='moment not exists')
    if db.query(Collect).filter_by(moment_id=moment_id, operator_user_id=current_user.id).first():
        # 重复收藏
        raise BaseError(msg='already collect')
    collect = Collect(
        operator_user_id=current_user.id,
        moment_id=moment_id,
        create_time=datetime.datetime.now()
    )
    db.add(collect)
    db.commit()
    db.flush()
    return BaseResponse(data=CollectOutSchema.from_orm(collect))


@moment_router.put('/moments/modify/{moment_id}')
async def modify(moment_id=Path(...), time_str=Query(...), db: Session = Depends(get_db)):
    moment = db.query(Moment).filter_by(id=moment_id).first()
    moment.publish_time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M")
    db.commit()
    return BaseResponse(data=moment)
