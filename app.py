"""
File: app.py
Author: Mihir Bhaskar, Anna Wang, Jameson Carter

Desc: This file initializes the Dash app, combining all the components

Note: features will typically have three functions. One function in the presentationg folder
for the layout, a corresponding function with _cb in the application folder for the relevant
callback(s), and a corresponding function with _db in the database folder for writing to the DB 
"""

# =============================================================================
# Importing functions, libraries and set-up
# =============================================================================
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import dash_leaflet as dl
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import uuid

# Import the function that reads data from the DB
from AssetMappr.database.readDB import readDB

# Import the layout functions
from AssetMappr.presentation.landingPage import makeLandingPage
from AssetMappr.presentation.layout import makeLayout

# Import the callbacks from the application folder
from AssetMappr.application.showAssetInfo_cb import showAssetInfo_cb
from AssetMappr.application.showMap_cb import showMap_cb
from AssetMappr.application.submitRating_cb import submitRating_cb
from AssetMappr.application.submitNewAsset_cb import submitNewAsset_cb
from AssetMappr.application.suggestMissingAsset_cb import suggestMissingAsset_cb

# =============================================================================
# Initialize app
# =============================================================================

# Note: the stylesheet set here determines the theme for the app - see DBC themes
app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.FLATLY])
server = app.server

app.title = 'AssetMappr'

# Latlong for Uniontown - to be replaced later with generalised function for other communities
community_lat = 39.8993885
community_long = -79.7249338

# Load data from the postgreSQL database (this will eventually depend on community input chosen)
df, asset_categories, master_categories, master_value_tags = readDB(app)

# This column demarcates between assets read in from the DB and staged assets added by the user
# in the current session, so they can be displayed on the map in different colors and ratings for
# verified vs. staged assets can be distinguished
df['asset_status'] = 'Verified'

# =============================================================================
# Layout
# =============================================================================

# Create the app layout
app.layout = html.Div([

    # Represents the browser address (i.e. where you are in the page structure)
    dcc.Location(id='url', refresh=False),

    # This will take the output from the callback below to display the appropriate layout
    # I.e. the landing/welcome page, or the main home page of the app
    html.Div(id='page-content')

])

# Callback to provide the relevant content depending on the page in the app


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    # If we are on the landing page (first page users see)
    if pathname == '/':
        return makeLandingPage()

    # If the user navigates to the main home page of the app
    # Note: there is a link in the landing_page that takes users to the home page
    if pathname == '/home':
        return makeLayout(df, master_categories)

# =============================================================================
# Callbacks
# =============================================================================


# Applying all the callbacks, passing relevant inputs so they can be used in the callbacks
showMap_cb(app, df, asset_categories)
showAssetInfo_cb(app)
submitRating_cb(app)
submitNewAsset_cb(app, df, asset_categories)
suggestMissingAsset_cb(app)

# =============================================================================
# Run the app
# =============================================================================
if __name__ == '__main__':

    # If running locally for test, use this code
    app.run_server(debug=True)

    # If running on render, use code below
    # server.run(host="0.0.0.0")
