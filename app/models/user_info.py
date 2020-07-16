from . import Base, Session
import random
from sqlalchemy import Integer, String, SMALLINT, Column, DateTime, Boolean, ForeignKey
from datetime import datetime
from app.util import token_util
from sqlalchemy.orm import relationship


# from sqlalchemy import create_engine, MetaData
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
#
# uri = f"postgresql://zengqi:123456@39.107.77.70:5432/testdb"
# engine = create_engine(uri)
#
# metadata = MetaData(bind=engine)
# Base = declarative_base(bind=engine)
# # 建表
# Base.metadata.create_all(bind=engine)
# Session = sessionmaker(bind=engine)
# session = Session()
#
# print("create_all")
#
#
# def get_db_session():
#     return session
#
#
# def get_db():
#     try:
#         yield session
#     finally:
#         session.close()
#
#
# db_session = get_db_session()


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

    user_role = relationship('UserRole')

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

# Base.metadata.drop_all(bind=engine)
# 建表
# Base.metadata.create_all(bind=engine)
# print("完成！")
# user = db_session.query(UserInfo).filter(UserInfo.username == 'zengqi12').first()
# user.update(db_session, mobile='231321312312312312311', nickname='333qpweoqw')
# # db_session.add(user)
# # print(user.__str__)
#
# # db_session.query(UserInfo).delete()
# list = db_session.query(UserInfo).all()
# db_session.commit()
# for u in list:
#     print(u.username)
#     print(u.mobile)
#     print(u.nickname)
# engine.dispose()
