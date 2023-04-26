# -*- coding:utf-8 -*-
import datetime as dt
import time
import uuid
from enum import Enum


class ModelName(Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


def make_ok_resp(data=None, **kwargs):
    resp = {"code": 0, "message": "request succeed", "data": data}
    resp.update(kwargs)
    return resp


def generate_task_number():
    _date = dt.datetime.now()
    return f"{_date:%Y%m%d}{str(uuid.uuid4())[:6]}"


def retry(func, on_error, times, wait=0):
    for _ in range(times - 1):
        try:
            return func()
        except on_error:
            if wait > 0:
                time.sleep(wait)
            continue
    return func()
