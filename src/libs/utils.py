# -*- coding:utf-8 -*-
import datetime as dt
import uuid


def generate_task_number():
    _date = dt.datetime.now()
    return f"{_date:%Y%m%d}{str(uuid.uuid4())[:6]}"
