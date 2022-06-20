"""
File: showAssetInfo_Planner_cb
Author: Anna Wang

Desc: This file creates the callbacks that display information about the selected asset
on the map in the planner view.
      
This is linked to the showAssetInfo_Planner.py layout file, as well as the showMap_Planner_cb because 
the callbacks take inputs from the map click events (when a user clicks on an asset)

Input: 
    app: an initialized dash app
    
Output: 
    Callbacks relating to the showAssetInfo feature
     
"""
from dash.dependencies import Input, Output, State
from dash import html
import pandas as pd
import numpy as np

def showAssetInfo_Planner_cb(app):
    # Callback to fetch the asset name from the point clicked on the map
    # Note: this and all callbacks below rely on clickData that is defined in the
    # showMap_cb file. The map/graph contains customdata about each point
    @app.callback(
        Output('name', 'children'),
        [Input('graph-for-planner', 'clickData')])
    def display_asset_info(clickData):
        if clickData is None:
            return None
        else:
            # clickData is a JSON style dictionary, with the customdata field
            # containing a data frame with relevant information about the clicked point
            name = clickData['points'][0]['customdata'][0]
            return name

    # Callback to fetch the asset description
    @app.callback(
        Output('desOrScore', 'children'),
        [Input('graph-for-planner', 'clickData')])
    def display_asset_desc(clickData):
        if clickData is None:
            return None
        else:
            desOrScore = clickData['points'][0]['customdata'][1]
            return desOrScore

    # Callback to fetch the website
    @app.callback(
        Output('justificationOrComments', 'children'),
        [Input('graph-for-planner', 'clickData')])
    def display_asset_website(clickData):
        if clickData is None:
            return None
        else:
            justificationOrComments = clickData['points'][0]['customdata'][3]
            return justificationOrComments

    # Show the address. And clicking it will lead to google map direction page.
    @app.callback(
        Output('address', 'children'),
        [Input('graph-for-planner', 'clickData')])
    def display_asset_desc(clickData):
        if clickData is None:
            return None
        else:
            address = clickData['points'][0]['customdata'][2]
            return html.A(address, href='https://www.google.com/maps/dir/?api=1&AIzaSyDitOkTVs4g0ibg_Yt04DQqLaUYlxZ1o30&destination={}+PA'.format(address), target="_blank")
