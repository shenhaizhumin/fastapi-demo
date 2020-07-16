from . import Base
from sqlalchemy import Column, String, Integer


class Image(Base):
    __tablename__ = 'image'
    id = Column('id', Integer, primary_key=True, unique=True)
    file_name = Column('file_name', String)
    file_path = Column('file_path', String)
