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
import dash_bootstrap_components as dbc

from flask_sqlalchemy import SQLAlchemy
from AssetMappr.application.display_map_cb import display_map_cb
from AssetMappr.presentation.display_map import display_map
# app requires "pip install psycopg2" as well (ensure it is installed if running locally)

# Import the database functions
from AssetMappr.database import readDB

# Import the layout and callback components
from AssetMappr.presentation.layout import make_layout
from AssetMappr.application.display_table_cb import display_table_cb

# =============================================================================
# Initialize app
# =============================================================================
app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.SUPERHERO])
server = app.server

app.title = 'AssetMappr'

# Load data from the postgreSQL database
df, asset_categories, master_categories, master_value_tags = readDB()

# Create the app layout
app.layout = make_layout()

# Create the display table callback
display_table_cb(app, db)
display_map_cb(app, db)


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
