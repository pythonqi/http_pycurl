# -*- coding: utf-8 -*-

"""
http_pycurl.models

"""
import json
from urllib.parse import urlencode, urlparse, urlunparse

from .exceptions import InvalidURL
from .structures import CaseInsensitiveDict
from .utils import get_cookies_str


class PreparedRequest():
    """The exact data that will be sent to the server.

    """
    def __init__(self):
        self.method = None
        self.url = None
        self.headers = CaseInsensitiveDict()

    def __repr__(self):
        return '<PreparedRequest [%s]>' % (self.method)

    def prepare(self,
                method=None, url=None, headers=None,
                data=None, params=None, cookies=None):

        self.prepare_method(method)
        self.prepare_url(url, params)
        self.prepare_headers(headers)
        self.prepare_cookies(cookies)
        self.prepare_body(data)


    @staticmethod
    def _encode_params(data):
        """Turn dict to string
        :param data: dict
        :return: string
        """
        result = []
        for key, value in data.items():
            if isinstance(value, list):
                for x in value:
                    result.append((key, x))
            else:
                result.append((key, value))
        return urlencode(result)

    def prepare_method(self, method):
        self.method = method
        if self.method:
            self.method = self.method.upper()

    def prepare_url(self, url, params):
        url = url.lstrip()

        if not url.lower().startswith('http'):
            raise InvalidURL(f"Invalid URL {url}")

        scheme, netloc, path, _params, query, fragement = urlparse(url)

        enc_params = self._encode_params(params)
        if enc_params:
            if query:
                query = f'{query}&{enc_params}'
            else:
                query = enc_params

        url = urlunparse([scheme, netloc, path, _params, query, fragement])
        self.url = url

    def prepare_headers(self, headers):
        """Convert the header information to lowercase.
        """
        self.header_list = []
        if headers:
            for key, value in headers.items():
                self.headers[key] = value
                self.header_list.append(key + ':' + value)

    def prepare_cookies(self, cookies):
        """Set header cookies information.
        :param cookies: dict or None
        """
        if cookies:
            cookies_str = get_cookies_str(cookies)
            self.headers['Cookie'] = cookies_str
            self.header_list.append('cookie'+ ':' + cookies_str)

    def prepare_body(self, data):
        """Turn post data dict to string.
        :param data: a dict
        """
        self.data = urlencode(data)


class Request():

    def __init__(self,
                 method=None, url=None, headers=None,
                 params=None, data=None, cookies=None):

        params = {} if not params else params
        data = [] if not data else data
        headers = {} if not headers else headers

        self.method = method
        self.url = url
        self.headers = headers
        self.data = data
        self.params = params
        self.cookies = cookies


    def __repr__(self):
        return '<Request [%s]>' % (self.method)

    def prepare(self):
        p = PreparedRequest()
        p.prepare(
            method=self.method,
            url=self.url,
            headers=self.headers,
            data=self.data,
            params=self.params,
            cookies=self.cookies,
        )
        return p


class Response():

    def __init__(self):
        self.content = None

        self.status_code = None

        self.url = None

        self.headers = CaseInsensitiveDict()

        self.encoding = None

        self.cookies = {}

        self.request = None

    def __repr__(self):
        return '<Response [%s]>' % (self.status_code)


    @property
    def text(self):

        encoding = self.encoding

        if not self.content:
            return ''

        if self.encoding is None:
            encoding = 'utf-8'

        try:
            content = str(self.content, encoding, errors='replace')
        except:
            content = str(self.content, errors='replace')

        return content

    def json(self):
        return json.loads(self.text)