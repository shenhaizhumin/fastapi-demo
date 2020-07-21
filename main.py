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
from app.settings import error_code
from app.views.user_views import user_router
from app.views.upload_api import upload_router
from app.views.moment_api import moment_router
import time
from starlette.responses import StreamingResponse
from fastapi.logger import logger as fastapi_logger
from logging.handlers import RotatingFileHandler
import logging
import traceback

formatter = logging.Formatter(
    "[%(asctime)s.%(msecs)03d] %(levelname)s [%(thread)d] - %(message)s", "%Y-%m-%d %H:%M:%S")
handler = RotatingFileHandler('error.log', backupCount=0)
logging.getLogger("fastapi")
fastapi_logger.addHandler(handler)
handler.setFormatter(formatter)

app = FastAPI()
app.include_router(login_router)
app.include_router(gank_router)
app.include_router(user_router)
app.include_router(upload_router)
app.include_router(moment_router)


@app.exception_handler(BaseError)
async def unicorn_exception_handler(request: Request, exc: BaseError):
    fastapi_logger.error(exc.message)
    return JSONResponse(
        status_code=200,
        content={"message": exc.message, "code": exc.code},
    )


@app.middleware('http')
async def middleware(req: Request, call_next):
    start_time = time.time()
    resp: StreamingResponse = await call_next(req)
    process_time = time.time() - start_time
    resp.headers['process-time'] = str(process_time)
    return resp


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    fastapi_logger.error(exc.detail)
    return JSONResponse(
        # status_code=exc.status_code,
        content={"message": f"StarletteHTTPException:{exc.detail}", 'code': error_code},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    fastapi_logger.error(exc.detail)
    return JSONResponse(
        status_code=200,
        content={"message": f"{str(exc.detail)}", 'code': error_code},
    )


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8021)
