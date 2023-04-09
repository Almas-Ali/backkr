from backkr import Backkr
from backkr.template import Template
from backkr.urls import Request, Response
from backkr.http import CookiesManager
from datetime import datetime
import uuid

app = Backkr(__name__)

template = Template()
template.set_template_dir('templates')
cookies_manager = CookiesManager('mysecretkey')


class IndexMiddleware:
    def __init__(self, Request, Response):
        self.request = Request
        if self.request.path == '/':
            print('index_middlware')

    def status_code(self):
        return self.request.status_code


app.middlewares = [
    # add custom middlewares
    IndexMiddleware,
]

app.apply_middleware(Request, Response)

# TODO: Implement methods=['GET', 'POST'] handler in server.


# @app.route('/', methods=['GET', 'POST'])
# def index(request):
#     return template.render_template('index.html', time=datetime.now().strftime("%H:%M:%S"))


@app.route('/about', methods=['GET'])
def about(request):
    return template.render_template('about.html')


@app.route('/')
def index(request):
    response = Response('Hello, World!')
    cookies_manager.set_cookie('username', 'john')
    cookies_manager.set_cookie('session_id', str(uuid.uuid4()), expires=3600)
    cookies_manager.process_response(request, response)
    return template.render_string('''\
    <h1>{{ username }}</h1>
''', username=cookies_manager.get_cookie('username'))


@app.route('/profile')
def profile(request):
    username = cookies_manager.get_cookie('username')
    session_id = cookies_manager.get_cookie('session_id')
    response = Response(
        f'Welcome, {username}! Your session ID is {session_id}')
    cookies_manager.process_response(request, response)
    return response


@app.route('/logout')
def logout(request):
    cookies_manager.delete_cookie('username')
    cookies_manager.delete_cookie('session_id')
    response = Response('You have been logged out.')
    cookies_manager.process_response(request, response)
    return response


if __name__ == "__main__":
    app.run(debug=True)
