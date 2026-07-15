"""
Opal Standard Library - HTTP & Web / مكتبة الويب و HTTP

Web requests and HTTP functionality.
طلبات الويب ووظائف HTTP

Note: Uses urllib from standard library (no external deps).
ملاحظة: يستخدم urllib من المكتبة القياسية بدون مكتبات خارجية
"""

import urllib.request as _request
import urllib.parse as _parse
import urllib.error as _error
import json as _json


def get_module():
    """إرجاع دوال مكتبة HTTP / Return HTTP module functions"""
    return {
        'get': _http_get,
        'post': _http_post,
        'request': _http_request,
        'url_encode': _url_encode,
        'url_decode': _url_decode,
        'fetch': _http_get,
    }


class OpalResponse:
    """يمثل استجابة HTTP / Represents an HTTP response"""

    def __init__(self, status, body, headers):
        self.status = status
        self.body = body
        self.headers = headers

    def __getitem__(self, key):
        if key == 'status':
            return self.status
        if key == 'body':
            return self.body
        if key == 'headers':
            return self.headers
        return None

    def __repr__(self):
        return f"<Response status={self.status}>"


def _http_get(url, headers=None):
    """طلب GET / HTTP GET request"""
    try:
        req = _request.Request(str(url))
        if headers:
            for k, v in headers.items():
                req.add_header(k, v)
        with _request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode('utf-8')
            return OpalResponse(resp.status, body, dict(resp.headers))
    except _error.HTTPError as e:
        return OpalResponse(e.code, str(e.reason), {})
    except Exception as e:
        return OpalResponse(0, str(e), {})


def _http_post(url, data=None, headers=None):
    """طلب POST / HTTP POST request"""
    try:
        if data is None:
            post_data = b''
        elif isinstance(data, dict):
            post_data = _parse.urlencode(data).encode('utf-8')
        elif isinstance(data, str):
            post_data = data.encode('utf-8')
        else:
            post_data = str(data).encode('utf-8')

        req = _request.Request(str(url), data=post_data, method='POST')
        if headers:
            for k, v in headers.items():
                req.add_header(k, v)
        else:
            req.add_header('Content-Type', 'application/x-www-form-urlencoded')

        with _request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode('utf-8')
            return OpalResponse(resp.status, body, dict(resp.headers))
    except _error.HTTPError as e:
        return OpalResponse(e.code, str(e.reason), {})
    except Exception as e:
        return OpalResponse(0, str(e), {})


def _http_request(url, method='GET', data=None, headers=None):
    """طلب HTTP عام / General HTTP request"""
    try:
        method = str(method).upper()
        post_data = None
        if data is not None:
            if isinstance(data, dict):
                post_data = _parse.urlencode(data).encode('utf-8')
            else:
                post_data = str(data).encode('utf-8')

        req = _request.Request(str(url), data=post_data, method=method)
        if headers:
            for k, v in headers.items():
                req.add_header(k, v)

        with _request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode('utf-8')
            return OpalResponse(resp.status, body, dict(resp.headers))
    except _error.HTTPError as e:
        return OpalResponse(e.code, str(e.reason), {})
    except Exception as e:
        return OpalResponse(0, str(e), {})


def _url_encode(s):
    """ترميز URL / URL encode"""
    return _parse.quote(str(s))


def _url_decode(s):
    """فك ترميز URL / URL decode"""
    return _parse.unquote(str(s))
