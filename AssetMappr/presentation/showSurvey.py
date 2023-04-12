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


def survey_Planner():
    return html.Div([

        dbc.Row([

            dbc.Col(className="title-what",
                    children=[html.H5('Survey Response', style={'font-weight': 'bold'})], width=6)
        ]),


        dbc.Row([

            dbc.Col([
                html.H6(className='subtitle-for-dropdown',
                        children=['Asset'], style={'font-weight': 'bold'}),

                # Dropdown to choose assets to display on the map
                dcc.Dropdown(
                    id='choose-the-source',
                    options=[
                        {"label": "Existing Assets",
                         "value": 'Existing Assets'},
                        {"label": "Suggested 'Missing' Assets",
                         "value": 'Missing Assets'},
                        {"label": "All", "value": 'All'}],
                    value='Existing Assets',
                    multi=False,
                ),
                html.H5('What is your current use of the areas around the asset?',
                        style={'font-weight': 'bold'}),
                dcc.Graph(id='bar-chart-survey-for-planner'),


            ], width=6),

            dbc.Col([

                html.H6(className='subtitle-for-dropdown',
                        children=['Number of Response'],
                        style={"text-align": "center"}),


                html.H5(children=['8'],
                        style={"font-size": "60px", "text-align": "center"}),

                html.H5('What is your current use of the areas around the asset?'),
                dcc.Graph(id='pie-chart-survey-for-planner'),
            ], width=6),




        ]),



        html.Hr()

    ])
