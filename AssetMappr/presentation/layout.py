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
import dash
import pandas as pd
from dash import dcc
from dash import html
from AssetMappr.presentation.H1title import H1title
#from AssetMappr.presentation.display_map import display_map
import dash_bootstrap_components as dbc
import dash_leaflet as dl

from AssetMappr.presentation.rowTwo import rowTwoLeft, rowTwoRight
from AssetMappr.presentation.selectMap import selectMap
from AssetMappr.presentation.showMap import showMap
from AssetMappr.presentation.showRate import showRate
from AssetMappr.presentation.showWebsite import showWebsite

from AssetMappr.presentation.title_desc import title_desc
from AssetMappr.presentation.submit_new_asset import submit_new_asset
from AssetMappr.presentation.suggest_missing_asset import suggest_missing_asset

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

def make_layout(df, master_categories):

    return html.Div([
        dcc.Tabs([

            # Tab 1: Home page/view assets
            dcc.Tab(label='Community User View', children=[

                dbc.Row([
                    H1title(),
                ]),

                dbc.Row([

                  dbc.Col(
                        rowTwoLeft(),
                        width={'size': 6, "offset": 0, 'order': 1}
                    ),
                    dbc.Col(
                        submit_new_asset(master_categories),
                        width={'size': 6, "offset": 0, 'order': 2}
                    )
                ]),

                html.Br(),

                dbc.Row([
                    dbc.Col(
                        showMap(),
                        width={'size': 6, "offset": 0, 'order': 1}),

                    dbc.Col(
                        dbc.Table(id="main_table", children=[display_table()]),
                        width={'size': 6, "offset": 0, 'order': 2}),
                ]),
               
                dbc.Row([
                    dbc.Col(
                        selectMap(df),
                        width=6,
                    ),
                    dbc.Col(
                        suggest_missing_asset(master_categories),
                        width={'size': 6, "offset": 0, 'order': 2},
                        ),
                ]),
                
                html.Br(),
                
                dbc.Row([
                    dbc.Col(
                        showWebsite(),
                        width=6)
                ]),
                
                #not finished
                dbc.Row([
                    dbc.Col(
                        showRate(),
                        width=6)
                ])

            ]),

            # Tab 2: Add asset
            dcc.Tab(label='Planner View', children=[

                html.H5("Placeholder")

            ])

        ]),

    ])
