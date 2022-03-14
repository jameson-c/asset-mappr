"""
File: layout.py
Author: Mihir Bhaskar, Anna Wang, Jameson Carter

Desc: This file creates the main layout of the app
Input: 
    - Draws on the individual layout components, defined in separate .py files
    in the 'presentation' folder
    
Output:
    - A function called make_layout() that returns the layout section of the Dash app
    
"""
from enum import auto
import dash
import pandas as pd
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import dcc
from dash import html
from AssetMappr.presentation.H1title import H1title
from AssetMappr.presentation.display_map import display_map
import dash_bootstrap_components as dbc

from AssetMappr.presentation.title_desc import title_desc
from AssetMappr.presentation.submit_new_asset import submit_new_asset
from AssetMappr.presentation.display_table import display_table
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# =============================================================================
# Function that makes the layout of the app
# =============================================================================
mapbox_access_token = 'pk.eyJ1IjoicWl3YW5nYWFhIiwiYSI6ImNremtyNmxkNzR5aGwyb25mOWxocmxvOGoifQ.7ELp2wgswTdQZS_RsnW1PA'

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Connect to the Heroku postgreSQL database
server.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ilohghqbmiloiv:f4fbd28e91d021bada72701576d41107b78bc515ad0b1e94d934939fbce7b2e6@ec2-54-235-98-1.compute-1.amazonaws.com:5432/dmt6i1v8bv5l1'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)


def make_layout():
    df = pd.read_sql_table('assets_preloaded', con=db.engine)

    return html.Div([
        dcc.Tabs([

            # Tab 1: Home page/view assets
            dcc.Tab(label='Community User View', children=[

                # title_desc(),
                # title:
                dbc.Row([
                    H1title(),
                ]),
                dbc.Row([
                        dbc.Col(
                            html.Div("Explore your community! Search the map for assets in your town.",
                                     style={'font-family': 'Gill Sans', "border": "2px black solid", 'border-color':
                                            'olivedrab', 'background': '#edede8', 'color': 'Black', 'font_size': '26px',
                                            'text-align': 'center'}), width={'size': 6, "offset": 0, 'order': 1}
                        ),
                        dbc.Col(
                            html.Div("CLICK HERE to add to the inverntory!",
                                     style={'background': 'olivedrab', 'color': 'Black',
                                            'font-family': 'Gill Sans', 'font_size': '20px',
                                            'text-align': 'center'}), width={'size': 6, "offset": 0, 'order': 2}
                        )
                        ]),
                html.Br(),
                dbc.Row([
                    dbc.Col(
                        dcc.Graph(id='graph', config={'displayModeBar': True, 'scrollZoom': True},
                                  style={'background': '#00FC87', 'height': '60vh'}),
                        width={'size': 6, "offset": 0, 'order': 1}),

                    dbc.Col(
                        dbc.Table(id="main_table", children=[display_table()]),
                        width={'size': 6, "offset": 0, 'order': 2}),
                ]),
                html.Br(),
                dbc.Row([
                    dbc.Col(
                        html.Div([
                        html.Label(children=['Select all assets the map should display:'], style={
                            'textDecoration': 'underline', 'fontSize': 20}),
                        dcc.Checklist(id="recycling_type", value=[x for x in sorted(df['category'].unique())],
                                      options=[{'label': x, 'value': x}
                                               for x in sorted(df['category'].unique())],
                                      labelClassName='mr-3 text-secondary')
                    ], style={'background': '#edede8', 'font-family': 'Gill Sans', 'textAlign': 'left', 'color': '#414744'}),
                     width = 6
                    )
                ]),
                html.Br(),
                dbc.Row([
                    dbc.Col(
                        html.Div([
                            html.Label(['Website:'], style={
                            'textDecoration': 'underline', 'fontSize': 20}),
                            html.Pre(id='web_link')
                            ], style={'background': '#edede8', 'font-family': 'Gill Sans', 'textAlign': 'left', 'color': '#414744'}),
                        width = 6)
                ]),
                html.Br(),
                #not finished
                dbc.Row([
                    dbc.Col(
                        html.Div([
                            html.Label(['Rate:(not finished yet)'], style={
                            'textDecoration': 'underline', 'fontSize': 20}),
                            html.Pre(id='rate')
                            ], style={'background': '#edede8', 'font-family': 'Gill Sans', 'textAlign': 'left', 'color': '#414744'}),
                        width = 6)
                    
                ])

                # display_table(),

                # submit_new_asset(),

                # display_map()


            ]),

            # Tab 2: Add asset
            dcc.Tab(label='Planner View', children=[

                html.H5("Placeholder")

            ])

        ]),



        # Interval for data update
        dcc.Interval(id='interval_pg', interval=1000, n_intervals=0)


    ])
