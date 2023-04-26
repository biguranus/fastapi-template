# -*- coding:utf-8 -*-
from typing import Union, Dict, List

from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse

from src.libs.auth import (
    oauth2_scheme,
    authenticate_user,
    create_access_token,
    get_current_active_user,
    authenticate_token,
)
from src.libs.exceptions import NotFound, UserError
from src.libs.logging import logger
from src.libs.utils import make_ok_resp, ModelName
from src.schemas.user import LoginUser, Token, LoginUserResponse

router = APIRouter(tags=["test"])


@router.get("/", tags=["test"])
def root():
    logger.debug("Just fot test!")
    return make_ok_resp()


@router.get("/error")
def test_exception():
    raise NotFound(message="test api not found")


@router.get("/items", dependencies=[Depends(authenticate_token)])
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}


@router.get("/me", response_model=LoginUserResponse)
async def read_me(current_user: LoginUser = Depends(get_current_active_user)):
    return make_ok_resp(data=current_user)


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise UserError
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


async def common_parameters(
    q: Union[str, None] = None, skip: int = 0, limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    def __init__(self, q: Union[str, None] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@router.get("/new/items")
async def read_items(commons: CommonQueryParams = Depends()):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response


@router.get("/new/users")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons


@router.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@router.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@router.post("/index-weights")
async def create_index_weights(weights: Dict[int, float]):
    return weights


@router.post("/login")
async def login(username: str = Form(), password: str = Form()):
    return make_ok_resp(data={"username": username})


# @router.post("/files")
# async def create_file(file: bytes = File()):
#     return {"file_size": len(file)}
#
#
# @router.post("/uploadfile")
# async def create_upload_file(file: UploadFile):
#     return {"filename": file.filename}


@router.post("/files", deprecated=True)
async def create_files(files: List[bytes] = File()):
    return {"file_sizes": [len(file) for file in files]}


@router.post("/uploadfiles")
async def create_upload_files(files: List[UploadFile]):
    return {"filenames": [file.filename for file in files]}


@router.post("/new/files")
async def create_file(
    file: bytes = File(), fileb: UploadFile = File(), token: str = Form()
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }
