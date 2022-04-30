import dash_core_components as dcc


def showMap():
    return dcc.Graph(id='graph', config={'displayModeBar': True, 'scrollZoom': True},
                     style={'background': '#00FC87', 'height': '60vh'})
