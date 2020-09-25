from fastapi import APIRouter
from datetime import timedelta
from app.settings import setting
from app.util.token_util import create_access_token
from app.response import BaseResponse, BaseError
from app.intercept import get_current_user
from fastapi import Depends, Path
import requests

banner_url = 'https://gank.io/api/v2/banners'

gank_router = APIRouter()


def get_resp(url):
    resp = requests.get(url)
    result = resp.json()
    if result['status'] == 100:
        return BaseResponse(data=result['data'])
    else:
        raise BaseError(msg='请求失败', code=setting.error_code)


@gank_router.get('/banner')
async def banner(user=Depends(get_current_user)):
    print(user.username)
    return get_resp(banner_url)


# 分类api <category_type>
category_url = 'https://gank.io/api/v2/categories/{category}'


@gank_router.get('/categories/{category}')
async def category(category=Path(...), user=Depends(get_current_user)):
    if category not in ['Article', 'GanHuo', 'Girl']:
        raise BaseError(msg="params must in ['Article','GanHuo','Girl']", code=setting.error_code)
    return get_resp(category_url.format(category=category))


# 分类数据api
category_data_url = 'https://gank.io/api/v2/data/category/{category}/type/{type}/page/{page}/count/{count}'


@gank_router.get('/category/{category}/type/{type}/page/{page}/count/{count}')
async def category(category=Path(...), type=Path(...), page=Path(...), count=Path(...), user=Depends(get_current_user)):
    return get_resp(category_data_url.format(category=category, type=type, page=page, count=count))
