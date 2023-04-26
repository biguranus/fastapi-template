# -*- coding:utf-8 -*-
from fastapi import APIRouter, Depends

from src.schemas.user import UserCreate, User, UserResponse
from src.models.users import Users
from src.schemas.response import BaseResponse
from src.libs.utils import make_ok_resp
from src.libs.auth import authenticate_token


router = APIRouter(
    prefix="/users", tags=["users"], dependencies=[Depends(authenticate_token)]
)


@router.get("/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/me")
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}


@router.post("/", response_model=User)
def create_user(user: UserCreate):
    return Users.create(user)


@router.get("/new/{user_id}", response_model=UserResponse)
def read_user_v2(user_id: int):
    result: Users = Users.get_user(user_id=user_id)
    return make_ok_resp(data=result.to_dict())
