from pydantic import BaseModel
from fastapi import Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


class PasswordRequestForm(OAuth2PasswordRequestForm):
    def __init__(self, username: str = Form(...), password: str = Form(...), mobile_captcha: str = Form(None)):
        self.username = username
        self.password = password
        self.mobile_captcha = mobile_captcha
