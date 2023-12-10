# Backkr - A backend framework the web 

Created by [**@Almas-Ali**](https://github.com/Almas-Ali)

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [License](#license)

## Introduction

Try out the [**examples/**](https://github.com/Almas-Ali/backkr/tree/master/examples/) folder to see how to use the framework.

## Installation

```bash
pip install backkr
```

## Usage

```python
from datetime import datetime

from backkr import (
    Backkr,
    HTMLResponse
)

app = Backkr()

@app.get('/')
async def index(request):
    return HTMLResponse(
        '<h1>Hello World, Time: {{ time }}</h1>',
        time=datetime.now().strftime("%H:%M:%S")
    )

@app.get('/{path}')
async def error_404(request):
    path = request.match_info.get('path')
    return HTMLResponse(f'''\
<center>
    <h1>404 Not Found</h1>
    <p>Page /{path} not found</p>
</center>
''')


if __name__ == "__main__":
    app.run(
        debug=True,
        host='127.0.0.1',
        port=8000
    )

```

## Documentation

[Website](https://almas-ali.github.io/backkr/)

## LICENSE

Licensed under the [**MIT LICENSE**](https://github.com/Almas-Ali/backkr/tree/master/LICENSE)
