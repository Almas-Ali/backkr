import os


class Template:
    def __init__(self):
        self.template_dir: str = './'

    def set_template_dir(self, template_dir):
        '''This method is used to set the template directory'''

        self.template_dir = template_dir

    def render_template(self, template, **kwargs):
        '''This method is used to render a template file'''
        # print(os.path.join(self.template_dir, template))

        try:
            with open(os.path.join(self.template_dir, template), 'r') as f:
                template = f.read()
            for key, value in kwargs.items():
                template = template.replace("{{ " + key + " }}", value)
            return template
        except FileNotFoundError:
            self.Error404()

    def render_string(self, template, **kwargs):
        '''This method is used to render a python template string'''

        for key, value in kwargs.items():
            template = template.replace("{{ " + key + " }}", value)
        return template

    def render_component(self, template, **kwargs):
        '''This method is used to render a python template string'''
        return template

    def Error404(self):
        return "<h1>404 Not Found</h1>"

    def Error500(self):
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
