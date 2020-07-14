from . import Base, engine
from sqlalchemy import Integer, String, SMALLINT, Column


class UserInfo(Base):
    __tablename__ = 'user'
    id = Column('id', Integer, primary_key=True)
    username = Column('username', String)

    # def create(self, **kwargs):
    #     for k, v in kwargs:
    #         self.__setattr__(k, v)


print("userinfo")
# 建表
Base.metadata.create_all(bind=engine)
