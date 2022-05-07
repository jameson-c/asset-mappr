"""
File: suggestMissingAsset_cb.py
Author: Mihir Bhaskar

Desc: This file creates the callbacks which interact with the suggest_missing_asset popup
      
      This is linked to the suggestMissingAsset.py layout file, as well as the suggestMissingAsset_db
      file in the Database folder, which writes the new user-entered info to the database

Input: 
    app: an initialized dash app
    
Output: 
    Callbacks relating to the suggest_missing_asset feature
     
"""
import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import dcc
from dash import html
import pandas as pd
import dash_leaflet as dl

from flask import request

from AssetMappr.database.suggestMissingAsset_db import suggestMissingAsset_db

def suggestMissingAsset_cb(app):
    
    # Callback to interact with the open and close buttons of the modal
    @app.callback(
        Output('suggest-missing-asset-modal', 'is_open'),
        [Input("open-suggest-missing-submit", 'n_clicks'), Input('close-suggest-missing-submit', 'n_clicks')],
        [State('suggest-missing-asset-modal', 'is_open')],
        )
    def toggle_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open
    
    # Callback to render the Leaflet map on which users will pin the location of the missing asset
    @app.callback(
        Output('missing-asset-map', 'children'),
        Input('suggest-missing-asset-modal', 'is_open')
        )
    def render_map_on_show(is_open):
        # This ensures that the map only renders if the modal is open, preventing screen resizing issues
        if is_open:
            return dl.Map([dl.TileLayer(), dl.LayerGroup(id='missing-layer')],
                      id='submit-missing-asset-map', 
                      # TODO: automate the centering of the map based on user input on community
                      zoom=14, center=(39.8993885, -79.7249338),
                      style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}
                     )
    
    # Callback to display the point the user has clicked on the map
    @app.callback(Output('missing-layer', 'children'), [Input('submit-missing-asset-map', 'click_lat_lng')])
    def map_click(click_lat_lng):
        return [dl.Marker(position=click_lat_lng, children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng)))]
        

    # Callback to take all the user-submitted info on the missing asset, and write it to the database
    @app.callback(
        Output(component_id='submit-suggestion-confirmation', component_property='children'),
        [Input('submit-suggestion-button', 'n_clicks')],
        [State('missing-user-name', 'value')],
        [State('missing-user-role', 'value')],
        [State('missing-asset-name', 'value')],
        [State('missing-asset-categories', 'value')],
        [State('missing-asset-desc', 'value')],
        [State('submit-missing-asset-map', 'click_lat_lng')]
        )
    def store_submitted_info(n_clicks, user_name, user_role, name, categories, desc, click_lat_lng):
        # If the 'Submit' button has not been clicked yet, return or do nothing
        if n_clicks == 0:
            return ''
        # If the submit button has been clicked, then write the info to the DB
        else:
            # Get the IP address from which this callback request was generated
            ip = request.remote_addr
            
            # Write to the database
            suggestMissingAsset_db(ip, user_name, user_role, name, categories, desc, click_lat_lng, community_geo_id=123)
                        
            return 'Suggestion for asset {} submited successfully! Thank you for helping out.'.format(name)
            
