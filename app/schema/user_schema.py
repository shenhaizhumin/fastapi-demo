from pydantic import BaseModel, Field
from datetime import datetime

mobile_pattern = "^1(3\d|4[4-9]|5[0-35-9]|6[67]|7[013-8]|8[0-9]|9[0-9])\d{8}$"
pwd_pattern = "(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])[a-zA-Z0-9]{8,20}"
user_name_pattern = "^[a-zA-Z0-9_+.-]+@?[a-zA-Z0-9_-]+\.?[a-zA-Z0-9]+$"
email_pattern = "^[a-zA-Z0-9_+.-]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9.]+$"


class UserInSchema(BaseModel):
    username: str = Field(None)
    email: str = Field(None, regex=email_pattern)
    mobile: str = Field(None, regex=mobile_pattern)

    nickname: str = Field(None)
    password: str = Field(...)
    avatar_url: str = Field(None)
    latest_ip: str = Field(None)


class UserOutSchema(BaseModel):
    id: int = Field(None)
    uid: str = Field(None)
    username: str = Field(None)
    email: str = Field(None)
    mobile: str = Field(None)

    nickname: str = Field(None)
    avatar_url: str = Field(None)
    latest_ip: str = Field(None)
    type_role: str = Field(None)
    latest_time: datetime = Field(None)
    access_token: str = Field(None)

    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    nickname: str = Field(None)
    password: str = Field(None)
    avatar_url: str = Field(None)
    moment_image: str = Field(None)
