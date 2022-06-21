"""
File: showMapf_Planner.py
Author: Anna Wang

Desc: This file returns an HTML Div with the asset map for planner views

The main map is created in showMap_Planner_cb in the application folder

Input

Output:
    - HTML Div, called in makeLayout()
"""
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from AssetMappr.presentation.showAssetInfo_Planner import showAssetInfo_Planner
import plotly.express as px


def showMap_Planner():
    return html.Div([
        
        html.H5('What would you like to see on the map?'),
        
        html.H6('Type of assets'),
        
        dcc.Dropdown(
                id='choose-the-source',
                options=[
                    {"label": "Existing Assets", "value": 'Existing Assets'},
                    {"label": "Suggested 'Missing' Assets", "value": 'Missing Assets'},
                    {"label": "All", "value": 'All'}],
                value='Existing Assets',
                multi=False
            ),
        
        html.H6('Type of map'),
        
        dcc.Dropdown(
            id='map-type',
            options=[
                {"label": 'Points', 'value': 'Points'},
                {'label': 'Heatmap', 'value': 'Heatmap'},
                {'label': 'Both', 'value': 'Both'}
                ],
            value='Points',
            multi=False
            ),
        
        dcc.Graph(id='graph-for-planner',
                  config={'displayModeBar': True, 'scrollZoom': True})

#        dbc.Row(showAssetInfo_Planner())

    ])
