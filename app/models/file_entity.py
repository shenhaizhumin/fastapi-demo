from . import Base
from sqlalchemy import Column, String, Integer, ForeignKey


class FileEntity(Base):
    __tablename__ = 'file_entity'
    id = Column('id', Integer, primary_key=True, unique=True)
    file_name = Column('file_name', String)
    file_path = Column('file_path', String)
    file_url = Column('file_url', String)
    moment_id = Column('moment_id', Integer, ForeignKey('moment.id'))
