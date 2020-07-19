from fastapi import APIRouter, Depends
from app.models import Session, get_db
from app.models.user_info import UserInfo
from app.models.moment import Moment, Collect, Comment
from app.intercept import get_current_user
from app.response import BaseError, BaseResponse
from app.schema.moment_schema import CollectInSchema, MomentInSchema, CommentInSchema, MomentOutSchema, \
    CommentOutSchema, CollectOutSchema
from app.models.file_entity import FileEntity
from app.util.date_util import released_time

moment_router = APIRouter()


@moment_router.get('/moments')
async def get_moments(current_user: UserInfo = Depends(get_current_user), db: Session = Depends(get_db)):
    '''
    查询当前用户的朋友圈列表
    :return:
    '''
    # user_id = current_user.id
    moments = db.query(Moment).filter_by().order_by(Moment.publish_time.desc()).all()
    results = []
    for m in moments:
        m.release_time = released_time(m.publish_time)
        results.append(MomentOutSchema.from_orm(m))
    # results = [MomentOutSchema.from_orm(m) for m in moments]
    return BaseResponse(data=results)


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
    )
    db.add(moment)
    db.commit()
    image_ids = schema.images
    # 绑定图片列表
    if image_ids and len(image_ids) > 0:
        for i in image_ids:
            file_entity = db.query(FileEntity).filter_by(id=i.id).first()
            if file_entity:
                file_entity.moment_id = moment.id
    # db.flush()
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
        moment_id=moment_id
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
        moment_id=moment_id
    )
    db.add(collect)
    db.commit()
    db.flush()
    return BaseResponse(data=CollectOutSchema.from_orm(collect))
