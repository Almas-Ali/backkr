import sys

sys.path.append('../../src/')

# App started from here.
from backkr import Backkr
from backkr.template import Template
from backkr.urls import Request, Response

from datetime import datetime

app = Backkr(__name__)

template = Template()
template.set_template_dir('templates')

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


@app.route('/', methods=['GET', 'POST'])
def index(request):
    return template.render_template('index.html', time=datetime.now().strftime("%H:%M:%S"))


@app.route('/about', methods=['GET'])
def about(request):
    return template.render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
