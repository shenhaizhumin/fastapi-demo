from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class CollectInSchema(BaseModel):
    moment_id: int = Field(...)


class CommentInSchema(BaseModel):
    moment_id: int = Field(...)
    content: str = Field(..., max_length=200)


class PublisherSchema(BaseModel):
    user_icon: str = Field(None, alias='avatar_url')
    user_nickname: str = Field(None, alias='nickname')
    user_id: int = Field(None, alias='id')

    class Config:
        orm_mode = True


class CollectOutSchema(BaseModel):
    id: int = Field(None)
    create_time: datetime = Field(None)
    # operator_user_id: int = Field(None)
    # user_nickname: str = Field(None)
    # user_avatar_url: str = Field(None)
    publisher: PublisherSchema = Field(None)
    moment_id: int = Field(None)

    class Config:
        orm_mode = True


class CommentOutSchema(BaseModel):
    id: int = Field(None)
    content: str = Field(None)
    publish_time: datetime = Field(None)
    # operator_user_id: int = Field(None)
    # user_nickname: str = Field(None)
    # user_avatar_url: str = Field(None)
    publisher: PublisherSchema = Field(None)
    moment_id: int = Field(None)

    class Config:
        orm_mode = True


class ImageInSchema(BaseModel):
    id: int = Field(...)


class ImageOutSchema(BaseModel):
    file_url: str = Field(None)

    class Config:
        orm_mode = True


class MomentInSchema(BaseModel):
    content: str = Field(...)
    content_url: str = Field(None)
    images: List[ImageInSchema] = Field(None)


class MomentOutSchema(BaseModel):
    '''
    user_icon = Column('user_icon', String)
    user_id = Column('user_id', Integer, ForeignKey('user.id'))
    publish_time = Column('publish_time', String, default=datetime.now())
    '''
    id: int = Field(None)
    content: str = Field(None)
    images: List[ImageOutSchema] = Field(None)
    content_url: str = Field(None)
    publish_time: datetime = Field(None)
    release_time: str = Field(None)
    publisher: PublisherSchema = Field(None, alias='publisher')
    comments: List[CommentOutSchema] = Field(None)
    collects: List[CollectOutSchema] = Field(None)

    class Config:
        orm_mode = True


class MomentByDaySchema(BaseModel):
    day_key: str = Field(None)
    year: int = Field(None)
    moments: list = Field(None)

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    user_nickname: str = Field(None, alias='nickname')
    user_moment_bg: str = Field(None, alias='moment_image')
    user_avatar_url: str = Field(None, alias='avatar_url')

    class Config:
        orm_mode = True
