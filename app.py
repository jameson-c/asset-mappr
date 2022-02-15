"""
File: app.py
Author: Mihir Bhaskar, Anna Wang, Jameson Carter

Desc: This file initializes the Dash app, combining all the components
"""

# =============================================================================
# Importing functions, libraries and set-up
# =============================================================================
import dash
import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import dcc
from dash import html

import sys, os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import pandas as pd
# app requires "pip install psycopg2" as well (ensure it is installed if running locally)


# Import the layout and callback components
from AssetMappr.presentation.layout import make_layout
from AssetMappr.application.display_table_cb import display_table_cb

# =============================================================================
# Initialize app
# =============================================================================  
app = dash.Dash(__name__)
server = app.server

# Connect to the Heroku postgreSQL database
server.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://acuyptgxqdqvjv:d34c46c553c1416005aceb276945d98e1902b112946add6a0dd76e040dd5b1de@ec2-54-208-139-247.compute-1.amazonaws.com:5432/d1prugfners9d"
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)    

app.title = 'AssetMappr'

app.layout = make_layout()

# Call the display table callback
display_table_cb(app, db)

app.run_server(debug=True, dev_tools_hot_reload=False)

