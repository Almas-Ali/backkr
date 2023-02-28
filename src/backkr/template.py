class Template:
    def __init__(self):
        pass

    def render_template(template, **kwargs):
        with open(template, "r") as f:
            template = f.read()
        for key, value in kwargs.items():
            template = template.replace("{{ " + key + " }}", value)
        return template

    def render_string(template, **kwargs):
        for key, value in kwargs.items():
            template = template.replace("{{ " + key + " }}", value)
        return template
    
    def render_component(self, template, **kwargs):
        '''This method is used to render a python template string'''
        return template

    def __str__(self):
        return "<Template object>"

    def __repr__(self):
        return "<Template object>"

    def __call__(self):
        return self
