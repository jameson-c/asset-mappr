"""
File: showMap.py
Author: Anna Wang, Mihir Bhaskar

Desc: This file returns an HTML Div with the main asset map and associated category selection

The main map is created in showMap_cb in the application folder

Input: master_categories: a list of the unique categories of assets

Output: 
    - HTML Div, called in makeLayout()
"""
import dash_core_components as dcc
from dash import html
import pandas as pd

def showMap(master_categories):
    return html.Div([
                # Checklist to select categories of assets to display on the map
                html.Div([
                        html.Label(children=['Select all assets the map should display:'], 
                                   style={'textDecoration': 'underline', 'fontSize': 20}),
                        # Checklist with options drawing from master_categories list
                        dcc.Checklist(id="recycling_type", 
                                      value=[x for x in master_categories],
                                      options=[{'label': str(x), 'value': x} for x in master_categories],
                                      )
                        ], style={'background': '#edede8', 'font-family': 'Gill Sans', 'textAlign': 'left'}
                ),
                
                html.Br(),
        
                # Container with the actual map, generated from a linked callback
                dcc.Graph(id='graph', config={'displayModeBar': True, 'scrollZoom': True},
                              style={'background': '#00FC87', 'height': '80vh'}),
        
          ])
