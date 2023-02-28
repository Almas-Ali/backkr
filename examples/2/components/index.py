from fronty.html import Element, Text, Break

# components
from components.layout import layout


def home(request, **data):

    _layout = layout(
        request=request,
        content=Element(
            'div',
            Element('h1', 'Home'),

            Text(
                f"""
                    Path: {request['PATH_INFO']} 
                    {Break()}
                    Method: {request['REQUEST_METHOD']}
                    
                """
            ),

        ).class_('container text-center')
    )

    return _layout

def about(request, **data):

    _layout = layout(
        request=request,
        content=Element(
            'div',
            Element('h1', 'About'),
        ).class_('container text-center')
    )

    return _layout