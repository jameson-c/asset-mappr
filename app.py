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
from dash import dash_table


# Import the function that reads master data from the DB
from AssetMappr.database.readDB import readMasters

# Import the layout functions
from AssetMappr.presentation.landingPage import makeLandingPage
from AssetMappr.presentation.layout import makeLayout

# Import the callbacks from the application folder
from AssetMappr.application.landingPage_cb import landingPage_cb
from AssetMappr.application.showAssetInfo_cb import showAssetInfo_cb
from AssetMappr.application.showMap_cb import showMap_cb
from AssetMappr.application.submitRating_cb import submitRating_cb
from AssetMappr.application.submitNewAsset_cb import submitNewAsset_cb
from AssetMappr.application.suggestMissingAsset_cb import suggestMissingAsset_cb
from AssetMappr.application.showSuggestEdit_cb import showSuggestEdit_initial_cb
from AssetMappr.application.submitSuggestEdit_cb import submitSuggestEdit_cb


from AssetMappr.application.showMap_Planner_cb import showMap_Planner_cb
from AssetMappr.application.catSummary_Planner_cb import catSummary_Planner_cb
from AssetMappr.application.tableDownload_Planner_cb import tableDownload_Planner_cb
from AssetMappr.application.topAssets_Planner_cb import topAssets_cb
# =============================================================================
# Initialize app
# =============================================================================

# Note: the stylesheet set here determines the theme for the app - see DBC themes
app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.SANDSTONE])
server = app.server

app.title = 'AssetMappr'


# Load master information from the postgreSQL database (this is standard info about the categories, etc. that is independent of the community selected)
master_categories, master_categories_desc, tagList_pos, tagList_neg, master_communities = readMasters()


# This column demarcates between assets read in from the DB and staged assets added by the user
# in the current session, so they can be displayed on the map in different colors and ratings for
# verified vs. staged assets can be distinguished
# df['asset_status'] = 'Verified'


# =============================================================================
# Layout
# =============================================================================

# Create the app layout
app.layout = html.Div([

    # Represents the browser address (i.e. where you are in the page structure)
    dcc.Location(id='url', refresh=False),

    # This will take the output from the callback below to display the appropriate layout
    # I.e. the landing/welcome page, or the main home page of the app
    html.Div(id='page-content'),

    # Storage containers to store the relevant community-filtered dataframes from the DB
    # This interacts with the community selection option in landingPage_cb.py, becuase it depends
    # on the community the user selects upon entering the app

    # Note: This info is accessed by several callbacks as an input
    # main data frame of assets
    dcc.Store(id='assets-df', storage_type='session'),
    # mapping of assets to categories
    dcc.Store(id='asset-categories-cnm', storage_type='session'),
    # base info about the selected community (name, geo_id, lat-long to center on)
    dcc.Store(id='selected-community-info', storage_type='session'),
    # data on all the 'missing' assets suggested by the community in the 'hopes for the future' tab
    dcc.Store(id='missing-assets-planner-view', storage_type='session'),
    # info on the ratings submitted by users about assets
    dcc.Store(id='rating-score-planner-view', storage_type='session'),
    # info on the 'value' tags associated with each of the ratings
    dcc.Store(id='rating-value-planner-view', storage_type='session'),


])

# Callback to provide the relevant content depending on the page in the app
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    # If we are on the landing page (first page users see)
    if pathname == '/':
        return makeLandingPage(master_communities)

    # If the user navigates to the main home page of the app
    # Note: there is a link in the landing_page that takes users to the home page
    if pathname == '/home':
        return  makeLayout(master_categories, tagList_pos, tagList_neg, master_categories_desc)


# =============================================================================
# Callbacks
# =============================================================================


# Applying all the callbacks, passing relevant inputs so they can be used in the callbacks
landingPage_cb(app, master_communities)
showMap_cb(app)
showAssetInfo_cb(app)
showSuggestEdit_initial_cb(app)
submitSuggestEdit_cb(app)
submitRating_cb(app, tagList_pos, tagList_neg)
submitNewAsset_cb(app)
suggestMissingAsset_cb(app)
showMap_Planner_cb(app)
catSummary_Planner_cb(app)
tableDownload_Planner_cb(app)
topAssets_cb(app)

# =============================================================================
# Run the app
# =============================================================================
if __name__ == '__main__':

    # If running locally for test, use this code
    app.run_server(debug=True)

    # If running on render, use code below
    # server.run(host="0.0.0.0")
