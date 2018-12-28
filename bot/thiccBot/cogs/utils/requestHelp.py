import aiohttp
import os

BACKEND_URL = os.environ['BACKEND_URL']
if not BACKEND_URL.endswith('/'):
    BACKEND_URL += '/'


def pad_url(url):
    if url.startswith('/'):
        url = url[1:]
    return BACKEND_URL + url

class requestHelp:
    """ This is helper that adds the base url of the backend to requests
    """
    @staticmethod
    def get(session, url, params=None, **kwargs) -> aiohttp.ClientResponse:
        return session.get(pad_url(url), params, **kwargs)
    
    @staticmethod
    def post(session, url, data=None, **kwargs) -> aiohttp.ClientResponse:
        return session.post(pad_url(url), data, **kwargs)

    @staticmethod
    def put(session, url, data=None, **kwargs) -> aiohttp.ClientResponse:
        return session.put(pad_url(url), data, **kwargs)

    @staticmethod
    def delete(session, url, **kwargs) -> aiohttp.ClientResponse:
        return session.delete(pad_url(url),**kwargs)
