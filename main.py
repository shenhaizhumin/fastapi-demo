import uvicorn
from fastapi import FastAPI, Request
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

app = FastAPI()
app.include_router(login_router)
app.include_router(gank_router)
app.include_router(user_router)
app.include_router(upload_router)


@app.exception_handler(BaseError)
async def unicorn_exception_handler(request: Request, exc: BaseError):
    return JSONResponse(
        status_code=200,
        content={"message": exc.message, "code": exc.code},
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        # status_code=exc.status_code,
        content={"message": f"StarletteHTTPException:{exc.detail}", 'code': error_code},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=200,
        content={"message": f"{str(exc)}", 'code': error_code},
    )


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8021)
