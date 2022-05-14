"""
File: submitRating_cb.py
Author: Anna Wang, Mihir Bhaskar

Desc: This file creates the callbacks which interact with the submitRating function
      
      This is linked to:
          - submitRating.py layout file
          - showMap_cb.py file, because it uses the map/graph to pull info about the clicked asset
            so that we know which asset the user is rating
          - submitRating.py in the database folder, which writes the rating to the SQL DB
         
Input: 
    app: an initialized dash app
    
Output: 
    Callbacks relating to the submit-rating feature
     
"""
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from AssetMappr.database.submitRating_db import submitRating_db


def submitRating_cb(app):
    @app.callback(
        Output(component_id='submit-rating-confirmation',
               component_property='children'),
        [Input('submit-rating-button', 'n_clicks')],
        [State('graph', 'clickData')],
        [State('rating-score', 'value')],
        [State('rating-comments', 'value')]
    )
    def submit_rating(n_clicks, clickData, rating_score, rating_comments):
        # This callback is only triggered when someone clicks the submit button
        if n_clicks == 0:
            return ''
        else:
            # Get Asset ID from the click data
            asset_id = clickData['points'][0]['customdata'][3]

            # Write the rating information to the staged ratings table in the DB
            submitRating_db(asset_id, rating_score, rating_comments)
            return dbc.Alert('Your review \" \n{} \" has been submitted - Thanks for sharing! '.format(rating_comments), dismissable=True, color='success')

    @app.callback(Output('rating-comments', 'value'),
                  Input('submit-rating-button', 'n_clicks')
                  )
    def clear_persistence(n_clicks):
        return " " if n_clicks else dash.no_update
