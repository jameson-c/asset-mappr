from dash import html

def showRate():
    return html.Div([
                html.Label(['Rate:(not finished yet)'], style={
                    'textDecoration': 'underline', 'fontSize': 20}),
                html.Pre(id='rate')
            ], style={'background': '#edede8', 'font-family': 'Gill Sans', 'textAlign': 'left', 'color': '#414744'}),
