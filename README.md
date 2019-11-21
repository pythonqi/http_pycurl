## http-pycurl Introduction

**http-pycurl** repackaged the [pycurl](https://github.com/pycurl/pycurl) for better use.

Thanks to the author of the [requests](https://github.com/psf/requests).Some code comes from requests.

The API it exposes is similar to the **requests**

### Installation

You should install pycurl first.

```shell
pip install http-pycurl
```

### Quickstart

#### Make a Request

Begin by importing the http_pycurl module.

```python
>>> import http_pycurl as requests
```

Currently only supports three request methods.

**GET**

```python
>>> r = requests.get('https://httpbin.org/get')
>>> r.status_code
200
>>> r.headers
{'Access-Control-Allow-Credentials': 'true', 'Access-Control-Allow-Origin': '*', 'Content-Encoding': 'gzip', 'Content-Type': 'application/json', 'Date': 'Thu, 21 Nov 2019 05:56:51 GMT', 'Referrer-Policy': 'no-referrer-when-downgrade', 'Server': 'nginx', 'X-Content-Type-Options': 'nosniff', 'X-Frame-Options': 'DENY', 'X-XSS-Protection': '1; mode=block', 'Content-Length': '264', 'Connection': 'keep-alive'}
>>> r.text
'{\n  "args": {}, \n  "headers": {\n    "Accept": "*/*", \n    "Accept-Encoding": "gzip, deflate", \n    "Host": "httpbin.org", \n    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"\n  }, \n  "origin": "xxx.xxx.xxx.xxx, xxx.xxx.xxx.xxx", \n  "url": "https://httpbin.org/get"\n}\n'
>>> r.json()
{'args': {}, 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Host': 'httpbin.org', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}, 'origin': 'xxx.xxx.xxx.xxx, xxx.xxx.xxx.xxx', 'url': 'https://httpbin.org/get'}
```

**POST**

```python
>>> post_data = {"foo": "bar"}
>>> r = requests.post("https://httpbin.org/post", data=post_data)
>>> r.json()
{'args': {}, 'data': '', 'files': {}, 'form': {'foo': 'bar'}, 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Content-Length': '7', 'Content-Type': 'application/x-www-form-urlencoded', 'Host': 'httpbin.org', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}, 'json': None, 'origin': 'xxx.xxx.xxx.xxx, xxx.xxx.xxx.xxx', 'url': 'https://httpbin.org/post'}
>>>
```

**HEAD**

```python
>>> r = requests.head("https://httpbin.org/get")
>>> r.status_code
200
>>> r.text
''
```

#### Passing Parameters In URLs

```python
>>> payload = {'key1': 'value1', 'key2': 'value2'}
>>> r = requests.get('https://httpbin.org/get', params=payload)
>>> r.url
'https://httpbin.org/get?key1=value1&key2=value2'
```

You can also pass a list of items as a value:

```python
>>> payload = {'key1': 'value1', 'key2': ['value2', 'value3']}
>>> r = requests.get('https://httpbin.org/get', params=payload)
>>> r.url
'https://httpbin.org/get?key1=value1&key2=value2&key2=value3'
```

#### Custom Headers

If you’d like to add HTTP headers to a request, simply pass in a `dict` to the `headers` parameter.

```python
>>> url = 'https://httpbin.org/get'
>>> headers = {'user-agent': 'http_pycurl/1.0.0'}
>>> r = requests.get(url, headers=headers)
>>> r.json()
{'args': {}, 'headers': {'Accept': '*/*', 'Host': 'httpbin.org', 'User-Agent': 'http_pycurl/1.0.0'}, 'origin': 'xxx.xxx.xxx.xxx, xxx.xxx.xxx.xxx', 'url': 'https://httpbin.org/get'}
```

#### Cookies

To send your own cookies to the server, you can use the `cookies` parameter:

```python
>>> url = 'https://httpbin.org/cookies'
>>> cookies = dict(cookies_are='working')
>>> r = requests.get(url, cookies=cookies)
>>> r.text
'{"cookies": {"cookies_are": "working"}}'
```

#### Timeouts

You can tell Requests to stop waiting for a response after a given number of seconds with the `timeout` parameter. The **timout** must be greater than 1 second.

```python
>>> url = 'https://httpbin.org/get'
>>> r = requests.get(url, timeout=1)
http_pycurl.exceptions.Timeout
```

#### Session

**Session** saves different cookies according to the domain name.And, it automatically sends cookies based on the domain name.

```python
>>> s = requests.Session()
>>> s.get('https://httpbin.org/cookies/set/sessioncookie/123456789')
>>> r = s.get('https://httpbin.org/cookies')
>>> print(r.text)
'{"cookies": {"sessioncookie": "123456789"}}'
```

### Why did I develop this package

When I crawled some websites, I found that they had a anit-spider by http message format.

Due to **requests'** http message format, the content of the website could not be obtained correctly.

However, **pycurl** can grab the right content. So I repackaged the **pycurl** for better use.

### Contact Me

If you have any questions,you can contact me by the following email：

luoyeqi@duoshoubang.cn