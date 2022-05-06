# Rating function callback

import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import dcc
from dash import html
import pandas as pd

from flask import request

from AssetMappr.database.submit_rating_db import submit_rating_db

def submit_rating_cb(app):
    
    @app.callback(
        Output(component_id='submit-rating-confirmation', component_property='children'),
        [Input('submit-rating-button', 'n_clicks')],
        [State('graph', 'clickData')],
        [State('rating-score', 'value')],
        [State('rating-comments', 'value')]
        )
    def submit_rating(n_clicks, clickData, rating_score, rating_comments):
        if n_clicks == 0:
            return ''
        else:
            
            # Get Asset ID from the click data
            asset_id = clickData['points'][0]['customdata'][3]
            
            submit_rating_db(asset_id, rating_score, rating_comments)
            return 'Your review has been submitted - thanks for sharing!'