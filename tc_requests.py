# -*- coding: utf8 -*-
import json
from requests.api import request

def main_handler(event, context):
    method = event.pop("method", "get")
    url = event.pop("url")
    res = request(method.lower(), url, **event)
    return {
        "status_code": res.status_code,
        "text": res.text,
        "headers": dict(res.headers.items()),
        "cookies": dict(res.cookies.items())
    }
