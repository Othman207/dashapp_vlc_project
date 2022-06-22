import dash
from dash import html
from dash import dcc
import os
import base64

image_filename = 'assets/vlcpics/vlc.jpg' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

vlc_image = os.path.join(os.getcwd(), 'vlc.jpg')

layout = html.Div([
html.H1(['Toyota VLC Vaccine Land Cruiser Evaluation Dashboard'],style={'text-align':'center','font-size':'5rem'}),
                           html.Hr(style={'background-color':'rgba(61,61,61,0.5)'}),
    # dcc.Location(id='url', refresh=False),
    # html.Div(id='page-content', children=[]),
            html.Div([
                html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                         style={"height": "700px", "width": "100%"})
            ])

])
