from . import Base, Session
from sqlalchemy import Integer, String, Column, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship


class Moment(Base):
    __tablename__ = 'moment'
    id = Column('id', Integer, primary_key=True)
    user_nickname = Column('user_nickname', String)
    content = Column('content', String)
    user_icon = Column('user_icon', String)
    user_id = Column('user_id', Integer, ForeignKey('user.id'))
    publish_time = Column('publish_time', String, default=datetime.now())
    # 链接地址
    content_url = Column('content_url', String)
    # 图片列表
    images = relationship('FileEntity')
    # 收藏列表
    collects = relationship('Collect')
    # 评论列表
    comments = relationship('Comment')
    # user info
    # user = relationship('UserInfo')


class Collect(Base):
    __tablename__ = 'collect'
    id = Column('id', Integer, primary_key=True)
    create_time = Column('create_time', DateTime, default=datetime.now())
    operator_user_id = Column('operator_user_id', Integer, ForeignKey('user.id'))
    user_nickname = Column('user_nickname', String)
    user_avatar_url = Column('user_avatar_url', String)
    moment_id = Column('moment_id', Integer, ForeignKey('moment.id'))
    # user = relationship('UserInfo', lazy='dynamic')


class Comment(Base):
    __tablename__ = 'comment'
    id = Column('id', Integer, primary_key=True)
    content = Column('content', String)
    publish_time = Column('publish_time', String, default=datetime.now())
    operator_user_id = Column('operator_user_id', Integer, ForeignKey('user.id'))
    user_nickname = Column('user_nickname', String)
    moment_id = Column('moment_id', Integer, ForeignKey('moment.id'))
    # user = relationship('UserInfo', lazy='dynamic')
