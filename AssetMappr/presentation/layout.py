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
#from AssetMappr.presentation.display_map import display_map
import dash_bootstrap_components as dbc
import dash_leaflet as dl

from AssetMappr.presentation.rowTwo import rowTwoLeft, rowTwoRight
from AssetMappr.presentation.selectMap import selectMap
from AssetMappr.presentation.showMap import showMap
from AssetMappr.presentation.showRate import showRate
from AssetMappr.presentation.showAssetInfo import showAssetInfo

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

def make_layout(df, master_categories):

    return html.Div([
        dcc.Tabs([

            # Tab 1: Page to view, rate, and upload assets
            dcc.Tab(label='Tell us about your community', children=[

                dbc.Row([

                  dbc.Col(
                      html.H4('Use the map below to view and select assets'),
                    ),
                  
                ]),

                html.Br(),

                dbc.Row([
                    dbc.Col(
                        showMap(master_categories),
                        ),
                    
                    dbc.Col([
                      html.H5('Information for selected asset:'),
                      showAssetInfo(),
                      html.Br(),
                      showRate(),
                      
                      html.Br(),
                      html.Br(),
                      html.Br(),
                      
                      submit_new_asset(master_categories),
                      
                    ]),

                ]),
               
                
                dbc.Row([
                    dbc.Col(
                        dbc.Table(id="main_table", children=[display_table()]),
                        width={'size': 6, "offset": 0, 'order': 2})
                        
                ]),

            ]),

            # Tab 2: Page to suggest 'missing' assets, share other thoughts about community dev
            dcc.Tab(label='What are your hopes for the future?', children=[
                suggest_missing_asset(master_categories),
            ])

        ]),

    ])
