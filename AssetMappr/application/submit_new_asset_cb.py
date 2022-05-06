"""
File: submit_new_asset_cb.py
Author: Mihir Bhaskar

Desc: This file creates the callbacks which interact with the submit_new_asset popup
      
      This is linked to the submit_new_asset.py layout file, as well as the submit_new_asset_db
      file in the Database folder, which writes the new user-entered asset info to the database

Input: 
    app: an initialized dash app
    
Output: 
    Callbacks relating to the submit-new-asset feature
     
"""
import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import dcc
from dash import html
import pandas as pd
import dash_leaflet as dl
import uuid

from flask import request

from AssetMappr.database.submit_new_asset_db import submit_new_asset_db


def submit_new_asset_cb(app):
    
    global df
    global asset_categories
    
    # Callback to interact with the open and close buttons of the modal
    @app.callback(
        Output('submit-asset-modal', 'is_open'),
        [Input('open-asset-submit', 'n_clicks'), Input('close-asset-submit', 'n_clicks')],
        [State('submit-asset-modal', 'is_open')],
        )
    def toggle_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open
    
    # Callback to render the Leaflet map on which users will pin the location of the asset
    @app.callback(
        Output('submit-asset-map', 'children'),
        Input('submit-asset-modal', 'is_open')
        )
    def render_map_on_show(is_open):
        # This ensures that the map only renders if the modal is open, preventing screen resizing issues
        if is_open:
            return dl.Map([dl.TileLayer(), dl.LayerGroup(id='layer')],
                      id='submit-asset-map', 
                      # TODO: automate the centering of the map based on user input on community
                      zoom=14, center=(39.8993885, -79.7249338),
                      style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}
                     )
    
    # Callback to display the marker point where the user has clicked on the map
    @app.callback(Output('layer', 'children'), [Input('submit-asset-map', 'click_lat_lng')])
    def map_click(click_lat_lng):
        return [dl.Marker(position=click_lat_lng, children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng)))]
        

    # Callback to take all the user-submitted info on the new asset, and write it to the database
    @app.callback(
        Output(component_id='submit-asset-confirmation', component_property='children'),
        [Input('submit-asset-button', 'n_clicks')],
        [State('user-name', 'value')],
        [State('user-role', 'value')],
        [State('asset-name', 'value')],
        [State('asset-categories', 'value')],
        [State('asset-desc', 'value')],
        [State('asset-website', 'value')],
        [State('submit-asset-map', 'click_lat_lng')]
        )
    def store_submitted_info(n_clicks, user_name, user_role, name, categories, desc, site, click_lat_lng):
        global df
        global asset_categories
        
        # If the 'Submit' button has not been clicked yet, return or do nothing
        if n_clicks == 0:
            return ''
        # If the submit button has been clicked, then write the info to the DB
        else:
            # Get the IP address from which this callback request was generated
            ip = request.remote_addr

            # Create a staged asset ID            
            staged_asset_id = str(uuid.uuid4()) 

            submit_new_asset_db(staged_asset_id, ip, user_name, user_role, name, categories, desc, site, click_lat_lng, community_geo_id=123)
            
            # TODO: Append this to the data frame loaded at the app initialization
            new_df_row = {'asset_id': staged_asset_id, 'asset_name': name,
                       'asset_status': 'Staged', 'community_geo_id': 123,
                       'source_type': 'User', 'description': desc, 'website': site,
                       'latitude': click_lat_lng[0], 'longitude': click_lat_lng[1]}
            df = df.append(new_df_row, ignore_index=True)
            
            for cat in categories:
                new_cat_row = {'asset_id': staged_asset_id, 'category': cat}
                asset_categories = asset_categories.append(new_cat_row)
            
            return '''Asset {} submited successfully! You should be able to see it on the main map after closing this screen. 
                   Thank you for helping out.'''.format(name)
            