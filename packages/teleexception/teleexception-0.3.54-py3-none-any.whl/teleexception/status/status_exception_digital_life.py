# -*- coding:utf-8 -*-
from .http_status_digital_life import HTTPStatusDigitalLife


class StatusExceptionDigitalLife(Exception):
    def __init__(self, status: HTTPStatusDigitalLife):
        self.code = status.value
        self.message = status.phrase
        self.details = status.description

    def __str__(self):
        return f'code: {self.code}, message: {self.message}, details: {self.details}'
