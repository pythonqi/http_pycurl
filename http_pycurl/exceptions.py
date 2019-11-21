# -*- coding: utf-8 -*-

class RequestException(Exception):

    def __init__(self, *args):
        self.args = args
        super().__init__(*args)

    def __str__(self):
        str = ''
        for arg in self.args:
            str += arg + ' '
        return str

class InvalidURL(RequestException):
    pass

class Timeout(RequestException):
    pass