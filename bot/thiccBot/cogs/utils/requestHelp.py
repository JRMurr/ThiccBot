import requests
import os
BACKEND_URL = os.environ['BACKEND_URL']
if not BACKEND_URL.endswith('/'):
    BACKEND_URL += '/'


def padURL(url):
    if url.startswith('/'):
        url = url[1:]
    return BACKEND_URL + url
class requestHelp:
    
    @staticmethod
    def get(url, params=None, **kwargs) -> requests.Response:
        return requests.get(padURL(url), params, **kwargs)
    
    @staticmethod
    def post(url, data=None, json=None, **kwargs) -> requests.Response:
        return requests.post(padURL(url), data, json, **kwargs)

    @staticmethod
    def put(url, data=None, **kwargs) -> requests.Response:
        return requests.put(padURL(url), data, **kwargs)

    @staticmethod
    def delete(url, **kwargs) -> requests.Response:
        return requests.delete(padURL(url),**kwargs)
