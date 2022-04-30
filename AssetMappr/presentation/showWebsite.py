from dash import html

def showWebsite():
    return html.Div([
                html.Label(['Website:'], style={
                    'textDecoration': 'underline', 'fontSize': 20}),
                html.Pre(id='web_link')
            ], style={'background': '#edede8', 'font-family': 'Gill Sans', 'textAlign': 'left', 'color': '#414744'}),