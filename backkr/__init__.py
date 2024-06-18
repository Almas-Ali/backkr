import asyncio
import time
import os
import sys
from typing import Any, Callable, List, Dict

from aiohttp import web
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from backkr.urls import Router, Request, Response
from backkr.template import (
    Template,
    HTMLResponse,
    JSONResponse,
    TemplateResponse,
    Redirect,
)
from backkr.logger import Logger, LogLevel, RouteLogger

__version__ = '0.0.4'

logger = Logger(level=LogLevel.DEBUG)


class FileSystemWatcher(FileSystemEventHandler):
    def __init__(self):
        super().__init__()

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            logger.debug(f'File {event.src_path} has been modified')
            logger.debug('Reloading server...')
            time.sleep(1)  # Give time for previous connections to close.
            # Restart the server.
            logger.debug('Server restarted')
            os.execv(sys.executable, [sys.executable] + sys.argv)


class Backkr:
    def __init__(self):
        self.app = web.Application()
        self.routes: List[web.RouteDef] = []
        self.host: str = "127.0.0.1"
        self.port: int = 8000
        self.debug: bool = False
        self.options: Dict[str, Any] = {}

    def get(self, path: str):
        def wrapper(func: Callable) -> Callable:
            self.routes.append(
                web.get(
                    path=path,
                    handler=func,
                    name=func.__name__,
                )
            )
            return func
        return wrapper

    def post(self, path: str):
        def wrapper(func: Callable) -> Callable:
            self.routes.append(
                web.post(
                    path=path,
                    handler=func,
                    name=func.__name__,
                )
            )
            return func
        return wrapper

    async def middleware(self, request: Request, handler: Callable) -> Response:
        '''This method is used to handle middleware'''
        return await handler(request)

    def _get_time_stamp(self):
        return time.strftime("%H:%M:%S", time.localtime())

    async def _run_web_server(self):
        '''This method is used to run the web server'''
        self.app.add_routes(self.routes)

        runner = web.AppRunner(self.app, access_log_class=RouteLogger)
        await runner.setup()

        site = web.TCPSite(runner, self.host, self.port)
        print('Backkr Development Server')
        print(f'Serving at http://{self.host}:{self.port}')
        print('Press Ctrl+C to stop')

        await site.start()

    async def run_other_task(self):
        while True:
            await asyncio.sleep(1)
            # print('Other Task is running..')

    def reload_server(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self._run_web_server())

    def run(
        self,
        *,
        debug: bool = False,
        host: str = "127.0.0.1",
        port: int = 8000,
        **options: Any,
    ) -> None:

        self.host = host
        self.port = port
        self.debug = debug
        self.options = options

        event_handler = FileSystemWatcher()
        observer = Observer()
        observer.schedule(event_handler, '.', recursive=True)
        observer.start()

        try:
            loop = asyncio.get_event_loop()
            loop.create_task(self._run_web_server())
            loop.run_until_complete(self.run_other_task())
            loop.run_forever()
        except KeyboardInterrupt:
            logger.warn('KeyboardInterrupt. Stopping server...')
            observer.stop()
        finally:
            observer.join()
            loop.close()
