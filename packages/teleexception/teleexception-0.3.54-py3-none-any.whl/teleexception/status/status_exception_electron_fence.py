# -*- coding:utf-8 -*-
from .http_status_electron_fence import HTTPStatusElectronFence


class StatusExceptionElectronFence(Exception):
    def __init__(self, status: HTTPStatusElectronFence):
        self.code = status.value
        self.message = status.phrase
        self.details = status.description

    def __str__(self):
        return f'code: {self.code}, message: {self.message}, details: {self.details}'
