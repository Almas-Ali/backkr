class Router:
    def __init__(self):
        self.routes = {}

    def route(self, path):
        def decorator(f):
            self.routes[path] = f
            return f
        return decorator

    def path(self, path):
        return self.routes[path]

    def __call__(self, path):
        return self.routes[path]

    def __str__(self):
        return "<Router object>"
