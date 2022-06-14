"""
File: landingPage_cb
Author: Mihir Bhaskar

Desc: This file creates the callback that selects the user's community and loads the
relevant data for that community, storing it in a dcc store object in the main app.py file
for use by relevant components of the app.

dcc.Store stores the data in the browser session of the user

This is linked to the landingPage.py layout file, as well as the app.py because 
the callbacks take inputs from the landingPage, and spits output into the output containers
stored in app.py. The reason the outputs are in app.py and not landingPage is to make it clear 
that it is a 'global' variable accessed by different callbacks.

Input: 
    app: an initialized dash app
    master_communities: the dataframe of unique communities and their associated info 
    
Output: 
    Callback that loads the relevant data for the community
"""
import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import dcc
from dash import html
import pandas as pd
import json

from AssetMappr.database.readDB import readDB # the readDB function does the SQL interaction

def landingPage_cb(app, master_communities):
    
    @app.callback(
        Output('assets-df', 'data'),
        Output('asset-categories', 'data'),
        Output('selected-community-info', 'data'),
        
        [Input('enterButton', 'n_clicks')],
        [State('community-select', 'value')]
        )
    def read_community_data(n_clicks, community_geo_id):
        if n_clicks != 0:
            
            # Calling readDB function from database, feeding in community_geo_id as input
            df, asset_categories = readDB(community_geo_id)
            
            # Subsetting master_communities dataframe to the correct row, so it has info only about
            # the chosen community
            nonlocal master_communities # define as nonlocal so this nested function knows to access it from the outer function
            selected_community = master_communities[master_communities['community_geo_id'] == community_geo_id]
            
            # dcc.Store data has to be in JSON format, so returning it using to_json
            # Three output containers, so three return outputs
            return (df.to_json(orient='split'), asset_categories.to_json(orient='split'),
                    selected_community.to_json(orient='split'))
        else:
            return None

