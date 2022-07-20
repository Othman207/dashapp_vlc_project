import dash
import dash_bootstrap_components as dbc
import datetime
import os
import dash_auth
from dash import html
from dash import dcc

scripts = ['https://cdnjs.cloudflare.com/ajax/libs/proj4js/2.3.6/proj4.js',
                    'https://code.highcharts.com/maps/highmaps.js',
                    'https://code.highcharts.com/maps/modules/exporting.js',
                    'https://code.highcharts.com/maps/modules/offline-exporting.js',
                    'https://code.highcharts.com/mapdata/countries/ne/ne-all.js',
                       'https://code.highcharts.com/highcharts.js',
                       'https://code.highcharts.com/modules/annotations.js',
                       'https://code.highcharts.com/modules/exporting.js',
                       'https://code.highcharts.com/modules/accessibility.js']

app = dash.Dash(__name__,suppress_callback_exceptions=True,external_scripts=scripts,external_stylesheets=[dbc.themes.BOOTSTRAP],meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])
app.title = "Vaccine Land Cruiser Evaluation Dashboard"


auth = dash_auth.BasicAuth(
     app,
    {'user1':'volta1734',
    'user2':'dosso1823',
     'inga1':'vlc123',
     'yuta1':'vlc243'}
)

