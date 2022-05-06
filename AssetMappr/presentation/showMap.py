import dash_core_components as dcc
from dash import html
import pandas as pd



def showMap(master_categories):
    return html.Div([
        dcc.Graph(id='graph', config={'displayModeBar': True, 'scrollZoom': True},
                      style={'background': '#00FC87', 'height': '80vh'}),
        
        html.Br(),
        
        html.Div([
                html.Label(children=['Select all assets the map should display:'], style={
                           'textDecoration': 'underline', 'fontSize': 20}),
                dcc.Checklist(id="recycling_type", value=[x for x in master_categories],
                              options=[{'label': str(x), 'value': x}
                                       for x in master_categories],
                              labelClassName='mr-3 text-secondary')
            ], style={'background': '#edede8', 'font-family': 'Gill Sans', 'textAlign': 'left'})
        
        ])
