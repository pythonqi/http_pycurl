# -*- coding: utf-8 -*-

"""
http_pycurl.api

"""

from . import sessions

def request(method, url, **kwargs):
    with sessions.Session() as session:
        return session.request(method=method, url=url, **kwargs)


def get(url, params=None, **kwargs):
    """Sends a GET request"""
    return request('get', url, params=params, **kwargs)

def post(url, data=None, **kwargs):
    """Sends a POST request"""
    return request('post', url, data=data, **kwargs)

def head(url, **kwargs):
    kwargs.setdefault('allow_redirects', False)
    return request('head', url, **kwargs)