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
                    children=[html.H5('Survey Analysis', style={'font-weight': 'bold'})], width=6)
        ]),


        dbc.Row([
            dbc.Col([
                html.H6(className='subtitle-for-dropdown',
                        children=['Asset'], style={'font-weight': 'bold', 'verticalAlign': 'top'}),

                dcc.Dropdown(
                    id='choose-the-source',
                    options=[
                        {"label": "Aquatorium",
                         "value": 'Existing Assets'},
                    ],
                    value='Existing Assets',
                    multi=False,
                    style={'verticalAlign': 'top'}
                ),]),

            dbc.Col([html.H6(children=['Number of Response'],
                             style={"text-align": "center", 'verticalAlign': 'top', 'font-weight': 'bold'}),


                     html.H6(id='response-number-survey-for-planner',
                             style={"font-size": "60px", "text-align": "center", 'verticalAlign': 'top'})])
        ]),

        dbc.Row([

            dbc.Col([
                html.H6('', style={"font-size": "60px"}),
                html.H6(id='q1-survey-for-planner',
                        style={'verticalAlign': 'top', 'font-weight': 'bold'}),

                dcc.Graph(id='bar-chart-survey-for-planner',
                          style={'verticalAlign': 'top'}),


            ], width=4),

            dbc.Col([
                html.H6(id='q2-survey-for-planner',
                        style={'verticalAlign': 'top', 'font-weight': 'bold'}),

                dcc.Graph(id='pie-chart-survey-for-planner',
                          style={'verticalAlign': 'top'}),


            ], width=4),

            dbc.Col([
                html.H6(id='q3-survey-for-planner',
                        style={'verticalAlign': 'top', 'font-weight': 'bold'}),

                dcc.Graph(id='bar-chart-q3-survey-for-planner',
                          style={'verticalAlign': 'top'}),

            ], width=4)

        ]),




        html.Hr()

    ])
