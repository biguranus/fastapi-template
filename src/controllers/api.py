# -*- coding:utf-8 -*-
from fastapi import APIRouter

from src.libs.utils import make_ok_resp
from src.libs.logging import logger
from src.libs.exceptions import NotFound


router = APIRouter(
    tags=["test"]
)


@router.get("/", tags=["test"])
def root():
    logger.debug("Just fot test!")
    return make_ok_resp()


@router.get("/error")
def test_exception():
    raise NotFound(message="test api not found")
