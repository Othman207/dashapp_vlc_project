from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import os

from rq import Queue
from worker import conn

# Connect to main app.py file
from app import app
#from app import server
# Connect to your app pages
from apps import home, niger, bf, sen

app.layout = html.Div([
# html.H1(['Toyota Vaccine Land Cruiser Evaluation Dashboard'],style={'text-align':'center','font-size':'5rem'}),
#                            html.Hr(style={'background-color':'rgba(61,61,61,0.5)'}),
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Niger Republique', href='/apps/niger'),
        dcc.Link('Burkina Faso', href='/apps/bf'),
        dcc.Link('Senegal', href='/apps/sen'),
    ], className="row"),
    html.Div(id='page-content', children=[])
    #         html.Div([
    #             html.Img(src="assets/vlcpics/vlc.jpg",
    #                      style={"height": "700px", "width": "100%"})
    #         ])

])


# app.clientside_callback(
#     ClientsideFunction(
#         namespace='clientside',
#         function_name='large_params_function',
#     ),
#     Output('map-1', 'children'),
#     Input('map-1', 'id'),
#     Input('map-data','data')
# )


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/niger':
        return niger.layout
    if pathname == '/apps/bf':
        return bf.layout
    if pathname == '/apps/sen':
        return sen.layout
    else:
        return home.layout

server = app.server
#server.secret_key = os.environ.get('secret_key', 'secret')

if __name__ == '__main__':
    app.run_server(debug=True)