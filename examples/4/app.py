from backkr import Backkr
from backkr.template import Template
from datetime import datetime

app = Backkr(__name__)

template = Template()
template.set_template_dir('templates')


@app.route('/', methods=['GET', 'POST'])
def index(request):
    return template.render_string(
        '<h1>Hello World, Time: {{ time }}</h1>',
        time=datetime.now().strftime("%H:%M:%S")
    )


if __name__ == "__main__":
    app.run(debug=True)