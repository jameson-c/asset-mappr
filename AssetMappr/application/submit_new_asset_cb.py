"""
File: submit_new_asset_cb.py
Author: Mihir Bhaskar

Desc: This file creates the callbacks which interact with the submit new asset popup
      
      This is linked to the submit_new_asset.py layout file, through the ids 'open-asset-submit',
      'submit-asset-map', 'close-asset-submit'

Input: 
    db: The database object
    app: an initialized dash app
Output: 
     
"""
import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import dcc
from dash import html
import pandas as pd
import dash_leaflet as dl


def submit_new_asset_cb(app, db):
    
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
    
    @app.callback(Output('layer', 'children'), [Input('submit-asset-map', 'click_lat_lng')])
    def map_click(click_lat_lng):
        return [dl.Marker(position=click_lat_lng, children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng)))]
        

    # Callback to take data coming from the submit-new-asset 
    @app.callback(
        Output(component_id='submit-asset-confirmation', component_property='children'),
        [Input('submit-asset-button', 'n_clicks')],
        [State('asset-name', 'value')],
        [State('asset-categories', 'value')],
        [State('asset-desc', 'value')],
        [State('asset-website', 'value')]
        )
    def store_submitted_info(n_clicks, name, categories, desc, site):
        if n_clicks == 0:
            return ''
        
        else:
            
            
            
            return 'Asset submited successfully'
            