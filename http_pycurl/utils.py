# -*- coding: utf-8 -*-

"""
http_pycurl.utils

"""
import re
import email
from io import StringIO

from .structures import CaseInsensitiveDict


def default_headers():
    return CaseInsensitiveDict({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
        'Accept-Encoding': ', '.join(('gzip', 'deflate')),
        'Accept': '*/*',
        'Connection': 'keep-alive',
    })


def get_encoding_from_headers(headers):
    """Returns encodings from given HTTP Header Dict.

    """
    content_type = headers.get('content-type')

    if not content_type:
        return None

    match = re.search('charset=(\S+)', content_type.lower())
    if match:
        encoding = match.group(1)
    else:
        encoding = 'iso-8859-1'

    return encoding

def get_headers_from_bytes(bytes):
    """Get headers from the response message"""
    hist = []
    lines = bytes.decode('iso-8859-1')
    while True:
        segment, body = lines.split('\r\n\r\n', 1)
        if body[:4] == "HTTP":
            hist.append(segment)
            lines = body
        else:
            break

    hist_cookies_str = get_cookies_from_hist(hist)

    request_line, headers_only = segment.split('\r\n', 1)
    message = email.message_from_file(StringIO(headers_only))

    headers = CaseInsensitiveDict()
    for key, value in message.items():
        if key not in headers:
            headers[key] = value
        else:
            headers[key] += '\n' + value

    if hist_cookies_str:
        if headers.get('Set-Cookie'):
            headers['Set-Cookie'] += '\n' + hist_cookies_str
        else:
            headers.setdefault('Set-Cookie', hist_cookies_str)
    return headers

def get_cookies_from_hist(hist):
    """Get cookie string from history response message"""
    result = []
    for item in hist:
        try:
            request_line, headers_only = item.split('\r\n', 1)
        except ValueError:
            return ''
        message = email.message_from_file(StringIO(headers_only))
        for key, value in message.items():
            if key.lower() == 'set-cookie':
                result.append(value)
    return '\n'.join(result)


def get_cookies_str(cookies):
    """Get cookies string from cookies dict."""
    l = [k + '=' + v for k, v in cookies.items()]
    return '; '.join(l)

def get_cookies_from_headers(headers):
    """Get cookies dict from headers' Set-Cookie"""
    cookies = {}
    cookie_list = None
    for k, v in headers.items():
        if k.lower() == 'set-cookie':
            cookie_list = headers[k].split('\n')

    if cookie_list:
        for line in cookie_list:
            forward, backward = line.split(';', 1)
            key, value = forward.split('=', 1)
            cookies[key] = value
    return cookies



