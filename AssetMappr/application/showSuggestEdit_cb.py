"""
File: showSuggestEdit_cb.py
Author: Anna Wang

Desc: This file creates the callbacks that display information about the original information of selected asset 
      in the suggestion edits. In other words, this file sets the default value of suggest edits form.

      
This is linked to the showAssetInfo.py layout file, the callbacks take inputs from the map click events (when a user clicks on an asset)

Input: 
    app: an initialized dash app
    
Output: 
    Callbacks relating to the show suggest eidit modal feature
"""

from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import html

from AssetMappr.database.submitRating_db import submitRating_db


def showSuggestEdit_initial_cb(app):
    @app.callback(
        [Output(component_id='suggested-name', component_property='value'),
         Output(component_id='suggested-desc', component_property='value'),
         Output(component_id='suggested-address', component_property='value'),
         Output(component_id='suggested-website', component_property='value'),
         Output('suggested-categories', 'value')],
        [Input('graph', 'clickData')]
    )
    def initial(clickData):
        if clickData is None:
            return None
        else:
            name = clickData['points'][0]['customdata'][0]
            desc = clickData['points'][0]['customdata'][1]
            address = clickData['points'][0]['customdata'][4]
            website = clickData['points'][0]['customdata'][2]
            cat = clickData['points'][0]['customdata'][5]
            return (name, desc, address, website, cat)
