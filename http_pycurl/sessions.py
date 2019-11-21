# -*- coding: utf-8 -*-

"""
http_pycurl.session

"""
import pycurl
from io import BytesIO
from urllib.parse import urlparse

from .models import Request, Response
from .utils import (
    default_headers, get_headers_from_bytes,
    get_cookies_from_headers, get_encoding_from_headers)
from .structures import CaseInsensitiveDict
from .exceptions import Timeout

def merge_setting(request_setting, session_setting):
    if request_setting is None:
        return session_setting

    merged_headers = CaseInsensitiveDict(list(session_setting.items()))
    merged_headers.update(list(request_setting.items()))
    
    none_keys = [k for k, v in merged_headers.items() if v is None]
    for key in none_keys:
        del merged_headers[key]
    
    return merged_headers


class Session(object):
    """A http_pycurl session.

    Provides cookie persistence.

    """
    def __init__(self):
        self.headers = default_headers()
        self.proxies = None
        self.cookies = CaseInsensitiveDict()
        self.__domain_cookies = CaseInsensitiveDict()
        self.__c = pycurl.Curl()

    def request(self, method, url,
                params=None, data=None, headers=None, cookies=None,
                proxies=None, timeout=30, allow_redirects=True):

        self.netloc = urlparse(url).netloc

        if headers:
            self.headers = headers

        if proxies:
            self.proxies = proxies

        if cookies:
            self.cookies = cookies
        elif self.__domain_cookies.get(self.netloc):
            self.cookies = self.__domain_cookies[self.netloc]

        req = Request(
            method=method,
            url=url,
            headers=merge_setting(headers, self.headers),
            params=params,
            data=data,
            cookies=merge_setting(cookies, self.cookies),
        )

        prep = req.prepare()

        proxies = proxies or {}

        send_kwargs = {
            'proxies': proxies,
            'timeout': timeout,
            'allow_redirects': allow_redirects
        }

        resp = self.send(prep, **send_kwargs)

        return resp


    def get(self, url, **kwargs):
        return self.request('GET', url, **kwargs)


    def post(self, url, data=None, **kwargs):
        return self.request('POST', url, data=data, **kwargs)

    def head(self, url, **kwargs):
        return self.request('HEAD', url, **kwargs)

    def send(self, request, **kwargs):
        """Send a given PreparedRequest."""

        proxies = kwargs.get('proxies')
        timeout = kwargs.get('timeout')
        allow_redirects = kwargs.get('allow_redirects')

        c = self.__c

        buffer = BytesIO()
        hdr = BytesIO()

        c.setopt(pycurl.URL, request.url)
        c.setopt(pycurl.WRITEDATA, buffer)
        c.setopt(pycurl.HTTPHEADER, request.header_list)
        c.setopt(pycurl.HEADERFUNCTION, hdr.write)
        c.setopt(pycurl.TIMEOUT, timeout)

        if proxies:
            proxy_host, proxy_port = proxies.split(':')
            c.setopt_string(pycurl.PROXY, proxy_host)
            c.setopt(pycurl.PROXYPORT, int(proxy_port))

        if allow_redirects:
            c.setopt(pycurl.FOLLOWLOCATION, True)

        if request.method == 'POST':
            c.setopt(pycurl.POSTFIELDS, request.data)

        if request.method == 'HEAD':
            c.setopt(pycurl.NOBODY, True)
        try:
            c.perform()
        except Exception as e:
            if e.args[0] == 28:
                raise Timeout

        http_code = c.getinfo(pycurl.HTTP_CODE)
        effective_url = c.getinfo(pycurl.EFFECTIVE_URL)

        body = buffer.getvalue()
        resp_headers = get_headers_from_bytes(hdr.getvalue())

        cookies = get_cookies_from_headers(resp_headers)
        self.__domain_cookies[self.netloc] = self.cookies = cookies


        response = Response()

        if body and body[:2] == b'\x1f\x8b': # gzip compress bytes
            import gzip
            body = gzip.decompress(body)

        response.request = request
        response.content = body
        response.status_code = http_code
        response.url = effective_url
        response.headers = resp_headers
        response.cookies = cookies
        response.encoding = get_encoding_from_headers(resp_headers)

        return response

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.headers = default_headers()
        self.proxies = None
        self.cookies = CaseInsensitiveDict()
        self.__domain_cookies = CaseInsensitiveDict()
        self.__c.close()
