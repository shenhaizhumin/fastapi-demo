from app.database import Base
from sqlalchemy import Integer, String, SMALLINT, Column


class UserInfo:
    user_id: int
    username: str
    password: str

    def __init__(self, user_id, username, pwd):
        self.username = username
        self.password = pwd
        self.user_id = user_id


class user_info(Base):
    __tablename__ = 'user'
    id = Column('id', Integer, primary_key=True)
    username = Column('username', String)

    # def create(self, **kwargs):
    #     for k, v in kwargs:
    #         self.__setattr__(k, v)
