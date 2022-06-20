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
        dbc.Row([
            dbc.Col(
                html.H4(
                    'Explore Your Community Here!'),
            ),
            dbc.Col(
                html.H4(
                    'Category Stat'),
            )

        ]),
        dbc.Row([
            dcc.Dropdown(
                id='choose-the-source',
                options=[
                    {"label": "Existing Assets", "value": 'Existing Assets'},
                    {"label": "Missing Assets", "value": 'Missing Assets'},
                    {"label": "All", "value": 'All'}],
                value='Existing Assets',
                multi=False
            ),
            dcc.Dropdown(
                id='choose-the-stat',
                options=[
                    {"label": "count_number", "value": 'count_number'}],
                value='count_number',
                multi=False
            ),

        ]),
        dbc.Row([
            dcc.Graph(id='graph-for-planner',
                      config={'displayModeBar': True, 'scrollZoom': True}),
            dcc.Graph(id='bar-chart-for-planner')

        ]),

        dbc.Row(showAssetInfo_Planner())

    ])
