from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/helloServer")
def hello(req: Request):
    return {
        'name': 'hello',
        'content': 'world'
        # 'remote_host':req.remote
    }


import uvicorn

# uvicorn.run(app)

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://zengqi:123456@39.107.77.70:5432/testdb')
Base = declarative_base(bind=engine)
Base.metadata.create_all(bind=engine)
