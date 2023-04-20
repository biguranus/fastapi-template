# -*- coding:utf-8 -*-


class APIException(Exception):
    http_code = 400
    error_code = 40000
    message = "APIException occured, bad request"

    def __init__(self, http_code=None, error_code=None, message=None):
        super().__init__()
        self.http_code = http_code or self.http_code
        self.error_code = error_code or self.error_code
        self.message = message or self.message

    def __str__(self):
        return f"error_code: {self.error_code}, message: {self.message}"

    def to_dict(self):
        return {
            "http_code": self.http_code,
            "error_code": self.error_code,
            "message": self.message,
        }

    __repr__ = __str__


class Unauthorized(APIException):
    http_code = 401


class Forbidden(APIException):
    http_code = 403


class NotFound(APIException):
    http_code = 404


class InternalError(APIException):
    http_code = 500


class ServiceUnavailable(APIException):
    http_code = 503
