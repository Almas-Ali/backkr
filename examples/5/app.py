from backkr import (
    Backkr,
    HTMLResponse,
    JSONResponse,
    TemplateResponse,
    Redirect,
)
import datetime

app = Backkr()


@app.get('/')
async def index(request):
    # print(request.headers)
    return TemplateResponse(template='home.html')


@app.get('/about')
async def about(request):
    print('No about found\nRedirecting to home')
    return Redirect('/')


@app.get('/time')
async def time(reqeust):
    return HTMLResponse(
        '<h1>Hello World, Time: {{ time }}</h1>',
        time=datetime.datetime.now().strftime("%H:%M:%S")
    )


@app.get('/json')
async def json(request):
    return JSONResponse({
        'name': 'Almas',
        'age': 16
    })


@app.get('/{path}')
async def error_404(request):
    path = request.match_info.get('path')
    return HTMLResponse(f'''\
<center>
    <h1>404 Not Found</h1>
    <p>Page /{path} not found</p>
</center>
''')


if __name__ == '__main__':
    app.run(
        debug=True,
        host='127.0.0.1',
        port=8000
    )
