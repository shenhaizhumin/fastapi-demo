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
import app.models.user_info

app = FastAPI()
app.include_router(login_router)
app.include_router(gank_router)


@app.exception_handler(BaseError)
async def unicorn_exception_handler(request: Request, exc: BaseError):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.message}"},
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
        status_code=400,
        content={"message": f"{str(exc)}", 'code': error_code},
    )


if __name__ == '__main__':
    uvicorn.run(app)
