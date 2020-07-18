from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Integer, String, SMALLINT, Column, DateTime, Boolean, ForeignKey
from datetime import datetime
from app.util import token_util
from sqlalchemy.orm import relationship
import random

# db_url = conf.get('db.url', 'pg_url')
uri = f"postgresql://zengqi:123456@39.107.77.70:5432/testdb"
engine = create_engine(uri)
metadata = MetaData(bind=engine)
Base = declarative_base(bind=engine)
# 建表
# Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


def get_db_session():
    return session


def get_db():
    try:
        yield session
    finally:
        session.close()


db_session = get_db_session()


class UserInfo(Base):
    __tablename__ = 'user'
    id = Column('id', Integer, primary_key=True)
    username = Column('username', String, default=token_util.generate_random_string(length=random.randint(4, 10),
                                                                                    type_='word'), unique=True)
    uid = Column('uid', String, default=token_util.generate_by_sha1_random, unique=True)
    nickname = Column('nickname', String)
    latest_time = Column('latest_time', DateTime)
    register_time = Column('register_time', DateTime, default=datetime.now())
    type_role = Column('type_role', SMALLINT)
    enable = Column('enable', Boolean, default=True)
    email = Column('email', String)
    latest_ip = Column('latest_ip', String)
    mobile = Column('mobile', String)
    avatar_url = Column('avatar_url', String)
    password = Column('password', String)
    role_id = Column('role_id', Integer, ForeignKey('user_role.id'))
    # avatar_id = Column('avatar_id', Integer, ForeignKey('image.id'))
    user_role = relationship('UserRole')

    # user_image = relationship('Image')

    @classmethod
    def create(cls, db: Session, **kwargs):
        user = cls(**kwargs)
        db.add(user)
        db.commit()
        return user

    def update(self, db: Session, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)
        db.commit()
        return self

    def __str__(self):
        return {'id': self.id, 'username': self.username, 'mobile': self.mobile, 'nickname': self.nickname,
                'register': self.register_time}


class UserRole(Base):
    __tablename__ = 'user_role'
    id = Column('id', Integer, primary_key=True, unique=True)
    role_type = Column('role_type', SMALLINT)
    desc = Column('desc', String)


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


class FileEntity(Base):
    __tablename__ = 'file_entity'
    id = Column('id', Integer, primary_key=True, unique=True)
    file_name = Column('file_name', String)
    file_path = Column('file_path', String)
    file_url = Column('file_url', String)
    moment_id = Column('moment_id', Integer, ForeignKey('moment.id'))


Base.metadata.drop_all(bind=engine)
# 建表
Base.metadata.create_all(bind=engine)
engine.dispose()
print('finish')
