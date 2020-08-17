from fastapi import APIRouter
import uvicorn as u
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import os

index_router = APIRouter()

index_router.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='../templates')


@index_router.get('/index')
async def index(req: Request):
    return templates.TemplateResponse('index.html', {'request': req})

