from . import Base
from sqlalchemy import Column, String, Integer, ForeignKey


class P2pMessage(Base):
    __tablename__ = 'p2p_message'
    id = Column('id', Integer, primary_key=True, unique=True)
    receive_id = Column('receive_id', Integer)  # 接收者id
    send_id = Column('send_id', Integer)  # 发送者 id
    msg = Column('msg', String)  # 消息内容
    receive_nickname = Column('receive_nickname', String)
    receive_avatar_url = Column('receive_avatar_url', String)
    post_time = Column('post_time', Integer)  # 发送时间
    # latest_msg = Column('latest_msg', String)
