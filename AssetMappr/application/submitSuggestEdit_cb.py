"""
File: submitSuggestEdit_cb.py
Author: Anna Wang

Desc: This file creates the callbacks which interact with the submitSuggestEdit popup
      
      This is linked to the showAssetInfo.py layout file, as well as the submitSuggest_db
      file in the Database folder, which writes the new user-entered asset suggestion edit info to the database

Input: 
    app: an initialized dash app
    
Output: 
    Callbacks relating to the submit-suggestion-edit feature
     
"""

from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from flask import request
import uuid

from AssetMappr.database.submitSuggest_db import submitSuggest_db


def submitSuggestEdit_cb(app):
    # Callback to take all the user-submitted info on the new asset, write it to the database, and reset the form
    @app.callback(
        # The output displays a confirmation message, and resets the values of all the input fields to blank/None
        Output(component_id='submit-suggest-confirmation', component_property='children'),  
        # The inputs of the text boxes and the lat long are all state-dependent on clicking the submit button
        [Input('submit-suggest-button', 'n_clicks')],
        [State('graph', 'clickData')],
        [State('suggested-name', 'value')],
        [State('suggested-desc', 'value')],
        [State('suggested-address', 'value')],
        [State('suggested-categories', 'value')],
        [State('suggested-website', 'value')],
        [State('current-status', 'value')]
        )
    def suggest_edit(n_clicks, clickData, name, desc, address, category, website, status):
        
        if n_clicks == 0:
            return ''
        else:
            edit_id =  str(uuid.uuid4())
            asset_id=clickData['points'][0]['customdata'][3]
            ip = request.remote_addr
            submitSuggest_db(edit_id, asset_id, name, desc, address, category, website, status,ip)
            return (dbc.Alert('''Submited successfully! Thank you for helping out.''', dismissable=True, color='success'))
            
           
            