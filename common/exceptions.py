from rest_framework.exceptions import APIException


class CustomException(APIException):
    status_code = 503
    default_detail = "Service temporarily unavailable, try again later."
    default_code = ""

    def __init__(self, detail=None, status_code=None):
        self.detail = detail
        self.status_code = status_code
