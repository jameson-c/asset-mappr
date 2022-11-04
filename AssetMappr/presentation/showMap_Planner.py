"""
File: showMap_Planner.py
Author: Anna Wang

Desc: This file returns an HTML Div with the asset map for planner views

The main map is created in showMap_Planner_cb in the application folder

Input

Output:
    - HTML Div, called in makeLayout()
"""
from turtle import width
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html


def showMap_Planner():
    return html.Div([

        dbc.Row([

            dbc.Col(className="title-what",
                    children=[html.H5('What would you like to see on the map?')], width=6),
            dbc.Col(className="title-what", children=[
                    html.H5('What type of category-wise summary would you like to see?')], style={'margin-left': 0}, width=5)
        ]),


        dbc.Row([

            dbc.Col([
                html.H6(className='subtitle-for-dropdown',
                        children=['Type of assets:']),

                # Dropdown to choose the type of assets to display on the map
                dcc.Dropdown(
                    id='choose-the-source',
                    options=[
                        {"label": "Existing Assets",
                         "value": 'Existing Assets'},
                        {"label": "Suggested 'Missing' Assets",
                         "value": 'Missing Assets'},
                        {"label": "All", "value": 'All'}],
                    value='Existing Assets',
                    multi=False
                ),

            ], width=3),

            dbc.Col([

                html.H6(className='subtitle-for-dropdown',
                        children=['Type of map:']),

                # Dropdown to decide the type of map to show
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
            ], width=3),


            dbc.Col([
                dbc.Row([
                    html.H6(className='subtitle-for-dropdown',
                            children=['Select statistic:'], id='select-statistic'),
                    dcc.Dropdown(
                        id='choose-the-stat',
                        options=[
                            {"label": "Number of existing assets",
                                "value": 'count_number'},
                            {"label": "Average of all ratings for assets",
                             "value": 'rating_avg'},
                            {"label": "Number of suggested (missing) assets",
                             "value": 'num_missing'}
                        ],
                        value='count_number',
                        multi=False
                    )

                ])

                # Dropdown to choose the type of category-wise stat user wants to see
            ], width=3)


        ]),

        dbc.Row([

            dbc.Col([
                # Graph object/placeholder for map created in callback
                dcc.Graph(id='graph-for-planner',
                          config={'displayModeBar': True, 'scrollZoom': True})
            ], width=6),
            # style={'background': '#00FC87', 'height': '70vh', 'width': '100vh'})

            dbc.Col([
                # Graph component to hold the graph created in the callback
                dcc.Graph(id='bar-chart-for-planner')
            ], width=6)

        ], class_name="g-0"),

        html.Hr()

    ])
