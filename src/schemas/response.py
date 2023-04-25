# -*- coding:utf-8 -*-
import uuid
from typing import Optional, Union

from pydantic import BaseModel


class BaseResponse(BaseModel):
    code: int = 0
    message: str = "succeed"
    request_id: Optional[str] = str(uuid.uuid1())
    data: Optional[Union[dict, list]]
