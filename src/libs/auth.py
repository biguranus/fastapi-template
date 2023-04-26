# -*- coding:utf-8 -*-
from datetime import timedelta, datetime

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from starlette import status

from src.libs.exceptions import UserInactive, AuthTokenFailed
from src.schemas.user import LoginUserInDB, TokenData, LoginUser

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

SECRET_KEY = "9977c7f2150d24b1c12652af5918c8a30f26d63cf3189550103a300f9d9612f9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def fake_hash_password(password: str):
    return "fakehashed" + password


def get_user(username: str):
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return LoginUserInDB(**user_dict)


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def fake_decode_token(token):
    return get_user(token)


async def authenticate_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise AuthTokenFailed
    except JWTError:
        raise AuthTokenFailed


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise AuthTokenFailed
        token_data = TokenData(username=username)
    except JWTError:
        raise AuthTokenFailed

    user = get_user(username=token_data.username)
    if user is None:
        raise AuthTokenFailed
    return user


async def get_current_active_user(current_user: LoginUser = Depends(get_current_user)):
    if current_user.disabled:
        raise UserInactive
    return current_user
