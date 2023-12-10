from backkr import Backkr
from backkr.urls import Router

# Components
from components.index import home

app = Backkr(__name__)
router = Router()
# app.router = router


@router.route('/')
def index(request):

    if request['REQUEST_METHOD'] == 'GET':
        print('GET')
    elif request['REQUEST_METHOD'] == 'POST':
        print('POST')
    else:
        print('OTHER')
        
    return home(request).render()


@router.route('/about')
def index2(request):
    return home(request).render()


if __name__ == '__main__':
    app.router = router
    app.run()
