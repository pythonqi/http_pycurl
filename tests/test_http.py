# -*- coding: utf-8 -*-

import unittest
import json
import http_pycurl as requests


class TestHttp(unittest.TestCase):

    def test_get(self):
        url = 'https://httpbin.org/get'
        resp = requests.get(url)
        data = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(url, data["url"])


    def test_get_with_headers(self):
        url = 'https://httpbin.org/get'
        headers = {
            "test": "test_get_with_headers"
        }
        resp = requests.get(url, headers=headers)
        data = resp.json()
        self.assertEqual(headers["test"], data["headers"]["Test"])

    def test_get_with_params(self):
        url = 'https://httpbin.org/get'
        params = {
            "test": "test_params"
        }
        resp = requests.get(url, params=params)
        data = resp.json()
        self.assertEqual('https://httpbin.org/get?test=test_params', data["url"])

    def test_get_with_proxies(self):
        url = 'https://httpbin.org/ip'
        resp = requests.get(url)
        data = resp.json()
        resp2 = requests.get(url, proxies='127.0.0.1:1080')
        data2 = resp2.json()
        self.assertNotEqual(data["origin"], data2["origin"])

    def test_post(self):
        url = 'https://httpbin.org/post'
        post_data = {"test": "test_post"}
        resp = requests.post(url, data=post_data)
        data = resp.json()
        self.assertDictEqual(post_data, data['form'])

    def test_head(self):
        url = 'https://httpbin.org/get'
        resp = requests.head(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.text, '')

    def test_session_cookie(self):
        url = 'https://httpbin.org/cookies/set/sessioncookie/123456789'
        s = requests.Session()
        s.get(url)
        self.assertDictEqual({'sessioncookie': '123456789'}, s.cookies)


    def test_send_cookie(self):
        url = 'https://httpbin.org/cookies'
        cookies = dict(cookies_are='working')
        resp = requests.get(url, cookies=cookies)
        data = resp.json()
        self.assertDictEqual(cookies, data['cookies'])

    def test_timeout(self):
        url = 'https://httpbin.org/get'
        try:
            requests.get(url, timeout=1)
        except Exception as e:
            from http_pycurl.exceptions import Timeout
            self.assertEqual(e.__class__, Timeout)