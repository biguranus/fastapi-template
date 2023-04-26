# -*- coding:utf-8 -*-
from typing import Optional, Union
from datetime import datetime

from pydantic import BaseModel, Field

from src.schemas.response import BaseResponse


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserResponse(BaseResponse):
    data: User


class LoginUser(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class LoginUserInDB(LoginUser):
    hashed_password: str


class LoginUserResponse(BaseResponse):
    data: LoginUser


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
