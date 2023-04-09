from http import cookies
import time
import uuid
import threading
from functools import wraps
from http.cookies import SimpleCookie
from backkr.urls import Response


class _Cache:
    '''Cache class to store function results'''

    def __init__(self):
        self.cache = {}

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value

    def clear(self):
        self.cache.clear()


cache = _Cache()


def cached(timeout=60):
    '''Decorator to cache function results for a given timeout'''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{args}:{kwargs}"
            cached_value = cache.get(key)
            if cached_value:
                return cached_value
            else:
                value = func(*args, **kwargs)
                cache.set(key, value)
                threading.Timer(timeout, cache.clear).start()
                return value
        return wrapper
    return decorator


class CookiesManager:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.cookies = cookies.SimpleCookie()

    def set_cookie(self, key, value, expires=None, max_age=None, domain=None, secure=False, http_only=False):
        self.cookies[key] = value

        if expires is not None:
            self.cookies[key]['expires'] = expires

        if max_age is not None:
            self.cookies[key]['max-age'] = max_age

        if domain is not None:
            self.cookies[key]['domain'] = domain

        if secure:
            self.cookies[key]['secure'] = True

        if http_only:
            self.cookies[key]['httponly'] = True

        self.cookies[key]['path'] = '/'

    def delete_cookie(self, key, domain=None):
        if domain is not None:
            self.cookies[key]['domain'] = domain

        self.cookies[key]['expires'] = time.strftime(
            '%a, %d-%b-%Y %H:%M:%S GMT', time.gmtime(0))

    def get_cookie(self, key):
        cookie = self.cookies.get(key)
        if cookie is not None:
            return cookie.value
        return None

    def process_response(self, request, response):
        for key, value in self.cookies.items():
            response.set_cookie(key, value.value, expires=value.get('expires'), max_age=value.get(
                'max-age'), domain=value.get('domain'), secure=value.get('secure'), httponly=value.get('httponly'))

    def process_request(self, request):
        if 'HTTP_COOKIE' in request.environ:
            self.cookies.load(request.environ['HTTP_COOKIE'])

    def __getitem__(self, key):
        return self.get_cookie(key)


# class Session:
#     def __init__(self, request):
#         self.request = request
#         self.session_id = None
#         self.session_data = {}
#         self.expires = None
#         self.load_session()

#     def load_session(self):
#         """
#         Load the session data from the request cookie or create a new session.
#         """
#         if 'HTTP_COOKIE' in self.request.environ:
#             cookies = SimpleCookie(self.request.environ['HTTP_COOKIE'])

#             if 'session_id' in cookies:
#                 self.session_id = cookies['session_id'].value

#                 if self.session_id in session_cache:
#                     session_data, expires = session_cache[self.session_id]

#                     if expires > time.time():
#                         self.session_data = session_data
#                         self.expires = expires
#                         self.request.session = self
#                         return
#         if not self.session_id:
#             self.create_session()

#     def create_session(self):
#         """
#         Create a new session with a unique session id and set the session cookie.
#         """
#         self.session_id = str(uuid.uuid4())
#         self.expires = time.time() + 3600
#         session_cache[self.session_id] = (self.session_data, self.expires)
#         response = Response()
#         response.set_cookie('session_id', self.session_id, max_age=3600)
#         self.request.session = self

#     def save_session(self):
#         """
#         Save the session data to the session cache.
#         """
#         session_cache[self.session_id] = (self.session_data, self.expires)

#     def __getitem__(self, key):
#         """
#         Get an item from the session data.
#         """
#         return self.session_data[key]

#     def __setitem__(self, key, value):
#         """
#         Set an item in the session data.
#         """
#         self.session_data[key] = value
#         self.save_session()

#     def __delitem__(self, key):
#         """
#         Delete an item from the session data.
#         """
#         del self.session_data[key]
#         self.save_session()
