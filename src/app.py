# -*- coding:utf-8 -*-
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from src.controllers import api, users


title = "FastAPI template Demo"
description = "FastAPI project template"
version = "0.0.1"
terms_of_service = "https://gateway.gongxingtech.com/"
contact = {
    "name": "gongxingtech",
    "url": "https://www.gongxingtech.com",
    "email": ""
}
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

    router = APIRouter(prefix="/api/v1")

    router.include_router(api.router)
    router.include_router(users.router)
    app.include_router(router)

    @app.get("/ping")
    async def ping():
        return "pong"

    return app
