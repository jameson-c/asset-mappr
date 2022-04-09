"""
File: app.py
Author: Mihir Bhaskar, Anna Wang, Jameson Carter

Desc: This file initializes the Dash app, combining all the components
"""

# =============================================================================
# Importing functions, libraries and set-up
# =============================================================================
import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html

import sys
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import pandas as pd
#from AssetMappr.application.display_map_cb import display_map_cb
#from AssetMappr.presentation.display_map import display_map
# app requires "pip install psycopg2" as well (ensure it is installed if running locally)


# Import the layout and callback components
from AssetMappr.presentation.layout import make_layout
from AssetMappr.application.display_table_cb import display_table_cb

from AssetMappr.application.submit_new_asset_cb import submit_new_asset_cb

# =============================================================================
# Initialize app
# =============================================================================
app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.SUPERHERO])
server = app.server

# Connect to the Heroku postgreSQL database
server.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ilohghqbmiloiv:f4fbd28e91d021bada72701576d41107b78bc515ad0b1e94d934939fbce7b2e6@ec2-54-235-98-1.compute-1.amazonaws.com:5432/dmt6i1v8bv5l1'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)

app.title = 'AssetMappr'

# Load category master values
master_categories = pd.read_sql_table('categories_master', con=db.engine)
master_categories = master_categories.values.tolist()

# Create the app layout
app.layout = make_layout()

# Create the display table callback
submit_new_asset_cb(app, db)
#display_table_cb(app, db)
#display_map(app)


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
