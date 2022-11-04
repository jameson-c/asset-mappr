"""
File: searchForName_cb.py TBD- change for the next version
Author: Anna Wang

Desc: This file creates the callback that display asstes what users search for in our database
      

Input: 
    app: an initialized dash app
    df: main data frame with assets to be displayed
    asset_categories: data frame with assets and their catagories (in separate df because 1 asset can have many cats)
    
Output: 
    Callbacks relating to the showMap feature
     
"""
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import pandas as pd
import requests
import json
import dash_html_components as html


def searchForName_cb(app, df, asset_categories):

    # Merge the assets and asset-category mappings into a single df
    # map_df = pd.merge(df, asset_categories, on='asset_id')

    @app.callback(
        Output('test', 'children'),
        Input('name-search-tab1', 'value')
    )
    def show(value):
        print(type(value))
        return value
