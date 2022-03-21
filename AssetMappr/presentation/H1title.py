from dash import html
import dash_bootstrap_components as dbc

def H1title():
    return dbc.Col(html.H1("Asset Inventory: Uniontown",
                           style={'color': 'olivedrab'},
                           className='text-center mb-4'),
                   width=12)
