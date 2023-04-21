# -*- coding:utf-8 -*-
import datetime as dt
import uuid


def make_ok_resp(data=None, **kwargs):
    resp = {"code": 0, "message": "request succeed", "data": data}
    resp.update(kwargs)
    return resp


def generate_task_number():
    _date = dt.datetime.now()
    return f"{_date:%Y%m%d}{str(uuid.uuid4())[:6]}"
