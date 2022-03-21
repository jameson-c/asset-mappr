from dash import html
import dash_bootstrap_components as dbc


def rowTwoLeft():
    return html.Div("Explore your community! Search the map for assets in your town.",
                    style={'font-family': 'Gill Sans', "border": "2px black solid", 'border-color':
                           'olivedrab', 'background': '#edede8', 'color': 'Black', 'font_size': '26px',
                           'text-align': 'center'})


def rowTwoRight():
    return html.Div("CLICK HERE to add to the inverntory!",
                    style={'background': 'olivedrab', 'color': 'Black',
                           'font-family': 'Gill Sans', 'font_size': '20px',
                           'text-align': 'center'})
