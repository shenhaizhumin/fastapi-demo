from fastapi import APIRouter, Depends
from app.models import Session, get_db
from app.models.user_info import UserInfo
from app.models.moment import Moment, Collect, Comment
from app.intercept import get_current_user
from app.response import BaseError, BaseResponse
from app.schema.moment_schema import CollectInSchema, MomentInSchema, CommentInSchema, MomentOutSchema, \
    CommentOutSchema, CollectOutSchema
from app.models.file_entity import FileEntity

moment_router = APIRouter()


@moment_router.get('/moments')
async def get_moments(current_user: UserInfo = Depends(get_current_user), db: Session = Depends(get_db)):
    '''
    查询当前用户的朋友圈列表
    :return:
    '''
    # user_id = current_user.id
    moments = db.query(Moment).filter_by().all()
    results = [MomentOutSchema.from_orm(m) for m in moments]
    return BaseResponse(data=results)


@moment_router.post('/moments/publish')
async def put_moment(schema: MomentInSchema, current_user: UserInfo = Depends(get_current_user),
                     db: Session = Depends(get_db)):
    '''
        发布动态
    :param schema:
    :param current_user:
    :param db:
    :return:
    '''
    user_id = current_user.id
    user_icon = current_user.avatar_url
    user_name = current_user.nickname
    moment = Moment(
        user_icon=user_icon,
        user_id=user_id,
        user_nickname=user_name,
        content=schema.content,
        content_url=schema.content_url,
    )
    db.add(moment)
    image_ids = schema.images
    # 绑定图片列表
    if image_ids and len(image_ids) > 0:
        for i in image_ids:
            file_entity = db.query(FileEntity).filter_by(id=i.id).first()
            if file_entity:
                file_entity.moment_id = moment.id
    db.commit()
    db.flush()
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
        user_nickname=user_name,
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
    collect = Collect(
        operator_user_id=current_user.id,
        user_avatar_url=current_user.avatar_url,
        user_nickname=current_user.nickname,
        moment_id=moment_id
    )
    db.add(collect)
    db.commit()
    db.flush()
    return BaseResponse(data=CollectOutSchema.from_orm(collect))
