from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from app.settings import test_db
from app.settings import setting

# db_url = conf.get('db.url', 'pg_url')
# uri = f"postgresql://{test_db['user']}:{test_db['password']}@{test_db['host']}:{test_db['port']}/{test_db['database']}"
uri = setting.DB_URI
engine = create_engine(uri)
metadata = MetaData(bind=engine)
Base = declarative_base(bind=engine)
# 建表
# Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


# session = Session()


def get_db():
    try:
        session = Session()
        yield session
    finally:
        session.close()
