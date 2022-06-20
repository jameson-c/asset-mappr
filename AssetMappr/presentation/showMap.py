"""
File: showMap.py
Author: Anna Wang, Mihir Bhaskar

Desc: This file returns an HTML Div with the main asset map

The main map is created in showMap_cb in the application folder


Output:
    - HTML Div, called in makeLayout()
"""
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc


def showMap():
    return html.Div([
   # Container with the actual map, generated from a linked callback
        dcc.Graph(id='graph', config={
                  'displayModeBar': True, 'scrollZoom': True})

    ])
