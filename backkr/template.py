from typing import Any, Dict
import os

from aiohttp import web

from backkr.logger import Logger, LogLevel

logger = Logger(level=LogLevel.DEBUG)


class Template:
    def __init__(self) -> None:
        self.template_dir: str = './'

    def set_template_dir(self, template_dir: str) -> None:
        '''This method is used to set the template directory'''

        self.template_dir = template_dir

    def render_template(self, template: str, **kwargs: Dict[Any, Any]) -> str:
        '''This method is used to render a template file'''
        # print(os.path.join(self.template_dir, template))

        try:
            with open(os.path.join(self.template_dir, template), 'r') as f:
                _template = f.read()
            for key, value in kwargs.items():
                _template = _template.replace("{{ " + key + " }}", value)
            return _template
        except FileNotFoundError:
            return self.Error404()

    def render_string(self, template, **kwargs):
        '''This method is used to render a python template string'''

        for key, value in kwargs.items():
            template = template.replace("{{ " + key + " }}", value)
        return template

    def render_component(self, template, **kwargs):
        '''This method is used to render a python template string'''
        return template

    def Error404(self):
        logger.error('404 Not Found')
        return "<h1>404 Not Found</h1>"

    def Error500(self):
        logger.error('500 Internal Server Error')
        return "<h1>500 Internal Server Error</h1>"

    def ErrorWithResponse(self, response):
        return f'''\
<h1>500 Internal Server Error</h1>
<p>{response}</p>
'''

    def __str__(self):
        return "<Template object>"

    def __repr__(self):
        return "<Template object>"

    def __call__(self):
        return self


def HTMLResponse(template: str, **kwargs):
    html = Template().render_string(template=template, **kwargs)
    return web.Response(
        text=html,
        content_type='text/html'
    )


def JSONResponse(json: dict):
    return web.json_response(json)


def TemplateResponse(template: str, dir: str = 'templates/', **kwargs: Dict[Any, Any]) -> web.Response:
    html = Template().render_template(
        template=os.path.join(dir, template),
        **kwargs
    )
    return web.Response(
        text=html,
        content_type='text/html'
    )


def Redirect(url: str):
    return web.HTTPFound(url)
