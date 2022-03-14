
import dash
import pandas as pd
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import dcc
from dash import html
from AssetMappr.presentation.display_map import display_map
import dash_bootstrap_components as dbc

from AssetMappr.presentation.title_desc import title_desc
from AssetMappr.presentation.submit_new_asset import submit_new_asset
from AssetMappr.presentation.display_table import display_table
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def H1title():
    return dbc.Col(html.H1("Asset Inventory: Uniontown",
                           style={'color': 'olivedrab'},
                           className='text-center mb-4'),
                   width=12)
