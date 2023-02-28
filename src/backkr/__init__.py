from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from backkr.http import Autoload
from dataclasses import dataclass
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
        self.path: str = path
        self.server = make_server(host, port, self.handle_request)

    def handle_request(self, environ, start_response):
        path = environ['PATH_INFO']
        query = parse_qs(environ['QUERY_STRING'])
        request = environ
        response = router(path)(request)
        start_response('200 OK', [('Content-type', 'text/html')])
        # print(f'path: {path}, request: {request}, response: {response}')
        return [bytes(response, 'utf-8')]

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
        print('Reloading server...')
        time.sleep(1)  # Give time for previous connections to close.
        os.execv(sys.executable, [sys.executable] + sys.argv)

    def check_file_changes(self):
        """
        Checks if any of the watched files have changed since the last check.
        If a file has changed, the server is reloaded.
        """
        while True:
            for file in self.watched_files:
                if os.stat(file).st_mtime > self.start_time:
                    self.reload_server()
            time.sleep(1)
            
    def is_watched_file(self, filename):
        """
        Checks if a filename has an extension in self.watched_extensions.
        """
        return any(filename.endswith(ext) for ext in self.watched_extensions)

    def find_watched_files(self, dir_path):
        """
        Recursively finds all Python files in a directory and its subdirectories.
        """
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if self.is_watched_file(file):
                    self.watched_files.append(os.path.join(root, file))
    
    def run(self):
        """
        Runs the server.
        """
        self.start_time = time.time()
        self.find_watched_files(self.path)

        try:
            _thread = threading.Thread(
                target=self.server.serve_forever)
            _thread.start()

            print(f'Serving at http://{self.host}:{self.port}')
            print('Press Ctrl+C to stop')

            _thread1 = threading.Thread(
                target=self.check_file_changes, daemon=True)
            _thread1.start()
            # print('Watching for file changes...')

            # _thread.join()
            # _thread1.join()

        except KeyboardInterrupt:
            print('Server stopped')

        except Exception as e:
            print(e)


@dataclass
class request:
    path: str
    query: Dict[str, Any]
    cookies: Dict[str, Any]
    headers: Dict[str, Any]
    body: Dict[str, Any]
    session: Dict[str, Any]


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


class Backkr:
    def __init__(self, file_path: str) -> None:
        self.__file_path = file_path

    @property
    def router(self):
        global router
        return router

    @router.setter
    def router(self, value):
        global router
        router = value

    def run(self, debug: bool = True, host: str = '127.0.0.1', port: int = 8000) -> None:
        server = ServerX(debug, host, port, self.__file_path)
        server.run()
