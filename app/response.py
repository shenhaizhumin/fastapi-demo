from pydantic import BaseModel
from fastapi import HTTPException


class BaseResponse:
    message: str
    code: int

    def __init__(self, msg='ok', code=200, data=None):
        self.message = msg
        self.code = code
        self.data = data


class BaseError(HTTPException):
    def __init__(self, msg=None, code=-200, status_code=None):
        self.message = msg
        self.code = code
        self.status_code = status_code
