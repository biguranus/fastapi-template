# -*- coding:utf-8 -*-
import uuid

from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.controllers import api, users
from src.libs.exceptions import APIException
from src.libs.logging import logger

title = "FastAPI template Demo"
description = "FastAPI project template"
version = "0.0.1"
terms_of_service = "https://gateway.gongxingtech.com/"
contact = {"name": "gongxingtech", "url": "https://www.gongxingtech.com", "email": ""}
openapi_url = "/api/v1/openapi.json"
tags_metadata = [
    {
        "name": "test",
        "description": "Just for test.",
    },
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]


def create_app():
    """
    创建 FastAPI 实例的工厂函数
    """
    app = FastAPI(
        title=title,
        description=description,
        version=version,
        terms_of_service=terms_of_service,
        contact=contact,
        openapi_url=openapi_url,
        openapi_tags=tags_metadata,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # db.Model.metadata.create_all(bind=db.get_engine())  # 自动创建表

    router = APIRouter(prefix="/api/v1")

    router.include_router(api.router)
    router.include_router(users.router)
    app.include_router(router)

    @app.get("/ping")
    async def ping():
        return "pong"

    @app.middleware("http")
    async def before_request(request: Request, call_next):
        request_id = request.headers.get("request_id", str(uuid.uuid1()))
        response = await call_next(request)
        response.headers["request_id"] = request_id
        logger.debug("before_request")
        return response

    @app.exception_handler(APIException)
    async def handle_error(request: Request, e: APIException):
        resp = {
            "code": e.error_code,
            "message": e.message,
        }
        return JSONResponse(status_code=e.http_code, content=resp)

    @app.on_event("startup")
    async def startup_event():
        logger.debug("Starting up!")

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.debug("Shutting down!")

    return app
