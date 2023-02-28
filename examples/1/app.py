from backkr import Backkr
from backkr.urls import Router
from backkr.template import Template
from backkr.http import Autoload
from fronty.html import Element

app = Backkr(__name__)
router = Router()
app.router = router


@router.route('/')
def index(request):
    return Template.render_template('html/index.html', title='Backkr')


@router.route('/contact')
def contact(request):
    _html = Element('div', Element('p', 'Hello World!'), id='container')
    return _html.render()


@router.route('/about')
def about(request):
    return Template.render_template('html/about.html', title='About')


if __name__ == '__main__':
    app.router = router
    app.run()
