import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from fastapi.responses import JSONResponse
from app.response import BaseError
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.views.client_login import login_router
from app.views.gank_api import gank_router
from app.settings import setting
from app.views.user_views import user_router
from app.views.upload_api import upload_router
from app.views.moment_api import moment_router
from app.views.ws_chat import ws_router
import time
# 路由
from starlette.routing import Route, WebSocketRoute
from app.views.ws_chat import Homepage, Echo
# from app.settings import logger

# 6BD4-5C9C-D45A-0873 E656-416D-6C0E-1E53 6AA5-4BEF-8817-3D37 007C-D06A-712C-6823
routes = [
    Route("/", Homepage),
    WebSocketRoute("/ws", Echo)
]
app = FastAPI(routes=routes)
app.include_router(login_router)
app.include_router(gank_router)
app.include_router(user_router)
app.include_router(upload_router)
app.include_router(moment_router)
app.include_router(ws_router)


@app.exception_handler(BaseError)
async def unicorn_exception_handler(request: Request, exc: BaseError):
    # logger.error(exc.message)
    return JSONResponse(
        status_code=200,
        content={"message": exc.message, "code": exc.code},
    )


# a={'scope': {'type': 'http', 'http_version': '1.1', 'server': ('127.0.0.1', 8021), 'client': ('127.0.0.1', 51866),
#              'scheme': 'http', 'method': 'POST', 'root_path': '', 'path': '/login', 'raw_path': b'/login', 'query_string': b'',
#              'headers': [(b'host', b'127.0.0.1:8021'),
#                          (b'connection', b'keep-alive'),
#                          (b'content-length', b'44'),
#                          (b'accept', b'application/json'),
#                          (b'origin', b'http://127.0.0.1:8021'),
#                          (b'user-agent', b'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3775.400 QQBrowser/10.6.4208.400'),
#                          (b'content-type', b'application/x-www-form-urlencoded'),
#                          (b'referer', b'http://127.0.0.1:8021/docs'),
#                          (b'accept-encoding', b'gzip, deflate, br'),
#                          (b'accept-language', b'zh-CN,zh;q=0.9')],
#              'fastapi_astack': <contextlib.AsyncExitStack object at 0x05D847D8>,
#   'app': <fastapi.applications.FastAPI object at 0x05CB2B20>},
# '_receive': <bound method RequestResponseCycle.receive of <uvicorn.protocols.http.h11_impl.RequestResponseCycle object at 0x05D847F0>>,
#                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           '_send': <function empty_send at 0x04EFF928>, '_stream_consumed': False, '_is_disconnected': False}
import traceback


@app.middleware('http')
async def middleware(req: Request, call_next):
    setting.INFO_LOGGER.info(f"scope:{req.scope}")
    start_time = time.time()
    try:
        resp = await call_next(req)
    except Exception as e:
        setting.ERROR_LOGGER.error(traceback.format_exc())
        return JSONResponse(content={'message': f"{e}", "code": -200})
    process_time = time.time() - start_time
    resp.headers['process-time'] = str(process_time)
    return resp


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    # logger.error(exc.detail)
    return JSONResponse(
        # status_code=exc.status_code,
        content={"message": f"StarletteHTTPException:{exc.detail}", 'code': setting.error_code},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    # logger.error(exc)
    return JSONResponse(
        status_code=200,
        content={"message": f"{str(exc)}", 'code': setting.error_code},
    )


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8021)
