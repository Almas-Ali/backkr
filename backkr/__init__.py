from backkr.urls import Router, Request, Response
from backkr.template import Template

from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from http import HTTPStatus
import traceback
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from typing import Callable, Dict, Any, List
import os
import sys
import time

from wsgiref.simple_server import make_server
import threading


# class Server:
#     def __init__(self, debug: bool = True, host: str = '127.0.0.1', port: int = 8000):
#         self.host: str = host
#         self.port: int = port
#         self.debug: bool = debug
#         self.server = make_server(host, port, self.handle_request)
#         self.autoload = Autoload('.')

#     def handle_request(self, environ, start_response):
#         path = environ['PATH_INFO']
#         request = parse_qs(environ['QUERY_STRING'])
#         response = router(path)(request)
#         start_response('200 OK', [('Content-type', 'text/html')])
#         return [bytes(response, 'utf-8')]

#     def serve_forever(self):
#         self.stop = False
#         while not self.stop:
#             self.handle_request()

#     def application(self, environ, start_response):
#         path = environ['PATH_INFO']
#         request = parse_qs(environ['QUERY_STRING'])
#         response = router(path)(request)
#         start_response('200 OK', [('Content-type', 'text/html')])
#         return [bytes(response, 'utf-8')]

#     def run(self):
#         try:
#             _thread = threading.Thread(
#                 target=self.server.serve_forever)
#             _thread.start()

#             _thread1 = threading.Thread(
#                 target=self.autoload.reload)
#             _thread1.start()

#             # _thread.join()
#             _thread1.join()

#             print(f'Serving at http://{self.host}:{self.port}')
#             print('Press Ctrl+C to stop')

#         except KeyboardInterrupt:
#             self.server.shutdown()
#             self.server.server_close()
#             print('Server stopped')

#         except Exception as e:
#             print(e)

#     def stop(self):
#         self.server.shutdown()


class ServerX:
    def __init__(self, debug: bool = True, host: str = '127.0.0.1', port: int = 8000, path: str = '.'):

        self.host: str = host
        self.port: int = port
        self.debug: bool = debug
        self.watched_extensions: List[str] = ['.py']
        self.watched_files: List[str] = []
        self.path: str = os.path.dirname(os.path.abspath(path))
        self.server = make_server(host, port, self.handle_request)

    def handle_request(self, environ, start_response):
        path = environ['PATH_INFO']
        query = parse_qs(environ['QUERY_STRING'])
        request = environ
        template = Template()
        try:
            # Send the request to the router
            response = router(path)['controller'](request)

        except KeyError:
            # If route not found
            response = template.Error404()

        except TypeError as TE:
            # If request not passed in controller
            if self.debug:
                response = template.ErrorWithResponse(response=str(TE))
            else:
                response = template.Error500()
        #################################################################
        print(type(response.res)) # TODO: Need to resolve the 500 Error here!
        start_response('200 OK', [('Content-type', 'text/html')])
        # print(f'path: {path}, request: {request}, response: {response}')
        return [bytes(response, 'utf-8')]
        ##################################################################

    def application(environ, start_response):
        """
        Your WSGI application code here.
        """
        response_body = b'Hello, world!'
        status = '200 OK'
        headers = [('Content-type', 'text/plain'),
                   ('Content-Length', str(len(response_body)))]
        start_response(status, headers)
        return [response_body]

    def reload_server(self):
        """
        Reloads the server by gracefully shutting down and then restarting.
        """
        print('Reloading server...\n')
        time.sleep(1)  # Give time for previous connections to close.
        # Restart the server.
        os.execv(sys.executable, [sys.executable] + sys.argv)

    def check_file_changes(self):
        """
        Checks if any of the watched files have changed since the last check.
        If a file has changed, the server is reloaded.
        """
        while True:
            # print('Checking for file changes...')
            for file in self.watched_files:
                # print(file)
                if os.stat(file).st_mtime > self.start_time:
                    self.reload_server()
                    print('File changed: ' + file)
            time.sleep(1)

    def is_watching_file(self, filename):
        """
        Checks if a filename has an extension in self.watched_extensions.
        """
        return any(filename.endswith(ext) for ext in self.watched_extensions)

    def find_watched_files(self, dir_path):
        """
        Recursively finds all Python files in a directory and its subdirectories.
        """
        for file in os.listdir(dir_path):
            if file == '__main__':
                continue
            file_path = os.path.join(dir_path, file)

            if os.path.isdir(file_path):
                self.find_watched_files(file_path)

            elif self.is_watching_file(file_path):
                self.watched_files.append(file_path)

    def run(self):
        """
        Runs the server.
        """
        self.start_time = time.time()
        self.find_watched_files(self.path)

        try:
            self._thread0 = threading.Thread(
                target=self.server.serve_forever)
            self._thread0.start()

            print('Backkr Development Server')
            print(f'Serving at http://{self.host}:{self.port}')
            print('Press Ctrl+C to stop')

            self._thread1 = threading.Thread(
                target=self.check_file_changes, daemon=True)
            self._thread1.start()
            print('Watching for file changes...')

            self._thread0.join()
            self._thread1.join()

        except KeyboardInterrupt:
            print('\nServer stopped')

        except Exception as e:
            print(e)

# class RequestHandler(BaseHTTPRequestHandler):

#     def do_GET(self):
#         path = urlparse(self.path).path
#         request = parse_qs(urlparse(self.path).query)
#         response = router(path)(request)
#         self.send_response(200)
#         self.send_header('Content-type', 'text/html')
#         self.end_headers()
#         self.wfile.write(bytes(response, 'utf-8'))

#     def do_POST(self):
#         path = urlparse(self.path).path
#         request = parse_qs(urlparse(self.path).query)
#         response = router(path)(request)
#         self.send_response(200)
#         self.send_header('Content-type', 'text/html')
#         self.end_headers()
#         self.wfile.write(bytes(response, 'utf-8'))

#     def do_QUIT(self):
#         self.send_response(200)
#         self.send_header('Content-type', 'text/html')
#         self.end_headers()
#         self.wfile.write(bytes('Server stopped', 'utf-8'))

#     def serve_forever(self):
#         self.stop = False
#         while not self.stop:
#             self.handle_request()

#     def handle_request(self):
#         try:
#             self.raw_requestline = self.rfile.readline()
#             if not self.raw_requestline:
#                 self.close_connection = 1
#                 return
#             if not self.parse_request():
#                 return
#             mname = 'do_' + self.command
#             if not hasattr(self, mname):
#                 self.send_error(501, "Unsupported method (%r)" % self.command)
#                 return
#             method = getattr(self, mname)
#             method()
#             self.wfile.flush()
#         except Exception as e:
#             print(e)
#             self.close_connection = 1
#             return

#     def stop_server(self):
#         self.stop = True

#     def start_server(self, debug: bool = True, host: str = '127.0.0.1', port: int = 8000):
#         try:
#             server = HTTPServer((host, port), RequestHandler)
#             print(f'Serving at http://{host}:{port}')
#             print('use <Ctrl-C> to stop')
#             server.serve_forever()
#         except KeyboardInterrupt:
#             print('Stoping server.')
#         except Exception as e:
#             print('Something went wrong with server ', e)


# class Backkr:
#     def __init__(self, file_path: str) -> None:
#         self.__file_path = file_path

#         logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', level=logging.DEBUG)
#         handler = logging.StreamHandler()
#         handler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s'))
#         logging.getLogger().handlers = [handler]

#     @property
#     def router(self):
#         global router
#         return router

#     @router.setter
#     def router(self, value):
#         global router
#         router = value

#     def run(self, debug: bool = True, host: str = '127.0.0.1', port: int = 8000) -> None:
#         server = ServerX(debug, host, port, self.__file_path)
#         server.run()


class Backkr:
    def __init__(self, name: str) -> None:
        self.name = name
        self.router = Router()
        global router
        router = self.router
        self.middlewares: List[Callable] = []

    def __call__(self, environ: Dict[str, Any], start_response: Callable) -> Any:
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def handle_request(self, request: Request) -> Response:
        response = Response()
        try:
            response = self.apply_middleware(request, response)
            if response.status_code == HTTPStatus.CONTINUE:
                print(response.status_code)
                return response
            handler = self.router.resolve(request)
            response = handler(request)
        except Exception as e:
            response = self.handle_exception(request, e)

        return response

    def handle_exception(self, request: Request, exception: Exception) -> Response:
        trace = traceback.format_exc()
        response = Response(
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            content_type="text/plain",
            body=trace.encode(),
        )
        return response

    def apply_middleware(self, request: Request, response: Response) -> Response:
        for middleware in self.middlewares:
            response = middleware(request, response)
            if response.status_code != HTTPStatus.CONTINUE:
                break
        return response

    def add_middleware(self, middleware: Callable) -> None:
        self.middlewares.extend(middleware)

    def route(self, path: str, methods: Union[str, List[str], Dict[str, str]] = "GET") -> Callable:
        # print(router.show_routes())

        def wrapper(func: Callable) -> Callable:
            self.router.add_route(path, func, methods)
            return func

        return wrapper

    def run(
        self,
        host: str = "localhost",
        port: int = 8000,
        debug: bool = False,
        **options: Any,
    ) -> None:
        from wsgiref.simple_server import make_server

        server = ServerX(
            host=host,
            port=port,
            debug=debug,
            path=self.name,
            **options,
        )
        server.run()
