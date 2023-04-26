# -*- coding:utf-8 -*-
from fastapi import status


class APIException(Exception):
    http_code = status.HTTP_400_BAD_REQUEST
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
    http_code = status.HTTP_401_UNAUTHORIZED


class Forbidden(APIException):
    http_code = status.HTTP_403_FORBIDDEN


class NotFound(APIException):
    http_code = status.HTTP_404_NOT_FOUND


class InternalError(APIException):
    http_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class ServiceUnavailable(APIException):
    http_code = status.HTTP_503_SERVICE_UNAVAILABLE


class UserEmailExisted(APIException):
    error_code = 40001
    message = "Email already registered"


class UserInactive(APIException):
    error_code = 40002
    message = "Inactive user"


class UserError(APIException):
    error_code = 40003
    message = "Incorrect username or password"


class AuthTokenFailed(Unauthorized):
    error_code = 40101
    message = "Could not validate credentials"


class UserNotFound(NotFound):
    error_code = 40401
    message = "User not found"
