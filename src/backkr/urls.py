from typing import Dict, Any, Callable
import urllib.parse
import http.client


class Router:
    def __init__(self) -> None:
        self.routes = {}

    def route(self, path: str, method: str = 'GET', name: str = None) -> Callable:
        def wrapper(func: Callable) -> Callable:
            self.add_route(path, func, method, name)
            return func
        return wrapper

    def path(self, path):
        return self.routes[path]

    def add_route(self, path, func: Callable, method='GET', name: str = None) -> None:
        self.routes[path] = {
            'controller': func,
            'name': func.__name__ if name is None else name,
            'method': method,
        }

    def show_routes(self) -> Dict[str, Any]:
        return self.routes

    def __call__(self, path) -> Callable:
        return self.routes[path]

    def __str__(self):
        return "<Router object>"


class Request:
    def __init__(self, environ: Dict[str, Any]):
        self.environ = environ

    @property
    def path(self) -> str:
        return self.environ.get('PATH_INFO', '')

    @property
    def method(self) -> str:
        return self.environ.get('REQUEST_METHOD', 'GET')

    @property
    def query_string(self) -> str:
        return self.environ.get('QUERY_STRING', '')

    @property
    def headers(self) -> Dict[str, Any]:
        return self.environ
    
    @property
    def cookies(self) -> Dict[str, Any]:
        return self.environ.get('HTTP_COOKIE', '')

    @property
    def status_code(self) -> int:
        return int(self.environ.get('STATUS_CODE', 200))

    def get_form_data(self) -> Dict[str, Any]:
        form_data = {}
        content_type = self.environ.get('CONTENT_TYPE', '')

        if 'application/x-www-form-urlencoded' in content_type:
            content_length = int(self.environ.get('CONTENT_LENGTH', 0))
            form_data = {k: v[0].decode() for k, v in urllib.parse.parse_qs(
                self.environ['wsgi.input'].read(content_length)).items()}

        return form_data


class Response:
    def __init__(self, status: int = 200, content_type: str = 'text/html'):
        self.status = status
        self.content_type = content_type
        self.headers = []

    def set_header(self, key: str, value: str):
        self.headers.append((key, value))

    def set_cookie(self, key: str, value: str, max_age: int = 3600):
        self.set_header(
            'Set-Cookie', f'{key}={value}; Max-Age={max_age}; HttpOnly; Path=/')

    def __call__(self, environ: Dict[str, Any], start_response):
        start_response(f'{self.status} {http.client.responses.get(self.status)}', [
                       ('Content-Type', self.content_type)] + self.headers)
        return []
