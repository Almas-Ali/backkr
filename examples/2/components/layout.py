from fronty.html import *


def layout(request, **data):
    return Html(
        Head(
            Title('Fronty'), # Page title
            Meta(charset='utf-8'), # Character encoding
            Meta(name='viewport', content='width=device-width, initial-scale=1'), # Responsive design

            # Bootstrap CSS
            Link(rel='stylesheet', href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css',
                 integrity='sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD', crossorigin='anonymous'),

        ),

        Body(

            # Main area of the page
            data.get('content', 'Empty content'),

            # Bootstrap JS
            Script(src='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js", integrity="sha384-w76AqPfDkMBDXo30jS1Sgez6pr3x5MlQ1ZAGC+nuZB+EYdgRZgiwxhTBTkF7CXvN', crossorigin='anonymous'),
        ),
    )
