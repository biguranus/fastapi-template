# -*- coding:utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.libs.utils import make_ok_resp
from src.libs.logging import logger
from src.libs.exceptions import NotFound, UserInactive, UserError, UserNotLogin
from src.schemas.user import LoginUser, LoginUserInDB


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
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


router = APIRouter(tags=["test"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")


@router.get("/", tags=["test"])
def root():
    logger.debug("Just fot test!")
    return make_ok_resp()


@router.get("/error")
def test_exception():
    raise NotFound(message="test api not found")


@router.get("/items")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}


def fake_hash_password(password: str):
    return "fakehashed" + password


def get_user(username: str):
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return LoginUserInDB(**user_dict)


def fake_decode_token(token):
    return get_user(token)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    login_user = fake_decode_token(token)
    if not login_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return login_user


async def get_current_active_user(current_user: LoginUser = Depends(get_current_user)):
    if current_user.disabled:
        raise UserInactive
    return current_user


@router.get("/me")
async def read_me(current_user: LoginUser = Depends(get_current_active_user)):
    return current_user


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise UserError
    login_user = LoginUserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == login_user.hashed_password:
        raise UserError

    return {"access_token": login_user.username, "token_type": "bearer"}
