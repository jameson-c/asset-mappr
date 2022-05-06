"""
File: app.py
Author: Mihir Bhaskar, Anna Wang, Jameson Carter

Desc: This file initializes the Dash app, combining all the components
"""

# =============================================================================
# Importing functions, libraries and set-up
# =============================================================================
import dash
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import dash_leaflet as dl
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import pandas as pd
from AssetMappr.application.display_map_cb import display_map_cb
import uuid
#from AssetMappr.presentation.display_map import display_map

# app requires "pip install psycopg2" as well (ensure it is installed if running locally)

# Import the database functions
from AssetMappr.database.readDB import readDB

# Import the layout and callback components
from AssetMappr.presentation.landing_page import landing_page

from AssetMappr.presentation.layout import make_layout

from AssetMappr.application.display_table_cb import display_table_cb
from AssetMappr.application.display_asset_info_cb import display_asset_info_cb
from AssetMappr.application.submit_rating_cb import submit_rating_cb

from AssetMappr.application.submit_new_asset_cb import submit_new_asset_cb
from AssetMappr.application.suggest_missing_asset_cb import suggest_missing_asset_cb


# =============================================================================
# Initialize app
# =============================================================================
app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.FLATLY])
server = app.server

app.title = 'AssetMappr'

# Latlong for Uniontown - to be replaced later with generalised function for other communities
community_lat = 39.8993885
community_long = -79.7249338

# Load data from the postgreSQL database (again, this will eventually depend on community input chosen)
df, asset_categories, master_categories, master_value_tags = readDB(app)
df['asset_status'] = 'Verified'

# Create the app layout
app.layout = html.Div([
    
    # Represents the browser address (i.e. where you are in the page structure)
    dcc.Location(id='url', refresh=False),
    
    # This will take the output from the callback below to display the appropriate layout
    # E.g. the landing/welcome page, or the main home page of the app
    html.Div(id='page-content')
    
    ])

# Callback to provide the relevant content depending on the page in the app
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    # If we are on the landing page (first page users see)
    if pathname == '/':
        return landing_page()
    
    # If the user navigates to the main home page of the app
    # Note: there is a link in the landing_page that takes users to the home page
    if pathname == '/home':
        
        # Make layout creates the main layout for the app
        return make_layout(df, master_categories)

# All the callbacks in the 'application' folder
submit_new_asset_cb(app)
suggest_missing_asset_cb(app)
#display_table_cb(app, db)
display_map_cb(app, df, asset_categories)
display_asset_info_cb(app)
submit_rating_cb(app)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
