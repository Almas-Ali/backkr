class request:
    def __init__(self, environ):
        self.environ = environ
        self.path = environ['PATH_INFO']
        self.method = environ['REQUEST_METHOD']
        self.query_string = environ['QUERY_STRING']
        self.headers = dict(environ['wsgi.input'].headers)
        self.body = environ['wsgi.input'].read()
        self.files = environ['wsgi.input'].files

    def get(self, key):
        return self.environ.get(key)

    def get_header(self, key):
        return self.headers.get(key)

    def get_body(self, key):
        return self.body.get(key)

    def get_file(self, key):
        return self.files.get(key)

    def get_query_string(self, key):
        return self.query_string.get(key)

    def get_path(self, key):
        return self.path.get(key)

    def get_method(self, key):
        return self.method.get(key)