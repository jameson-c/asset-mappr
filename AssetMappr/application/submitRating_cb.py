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
from dash import html

from AssetMappr.database.submitRating_db import submitRating_db


def submitRating_cb(app):
    @app.callback(
        Output(component_id='submit-rating-confirmation',
               component_property='children'),
        [Input('submit-rating-button', 'n_clicks')],
        [State('graph', 'clickData')],
        [State('rating-score', 'value')],
        [State('rating-comments', 'value')],
        [State('value-tag', 'value')]
    )
    def submit_rating(n_clicks, clickData, rating_score, rating_comments, value_tag):
        # This callback is only triggered when someone clicks the submit button
        if n_clicks == 0:
            return ''
        else:
            # Get Asset ID from the click data
            asset_id = clickData['points'][0]['customdata'][3]
            print(clickData)
            print(value_tag)

            # Write the rating information to the staged ratings table in the DB
            submitRating_db(asset_id, rating_score, rating_comments, value_tag)
            return dbc.Alert('Your review has been submitted - Thanks for sharing! ', dismissable=True, color='success')

    # Show the label: "How do you feel about XXXX(asset name)?"
    @app.callback(Output('HowDoYouFeel', 'children'),
                  Input('graph', 'clickData')
                  )
    def review_label(clickData):
        if clickData == None:
            return html.H5('After clicking the asset, you can rate it.')
        else:
            asset_name = clickData['points'][0]['customdata'][0]
            return html.H5('How do you feel about {}?'.format(asset_name))

    # clear after submitting
    @app.callback(Output('rating-comments', 'value'),
                  Input('submit-rating-button', 'n_clicks')
                  )
    def clear_persistence(n_clicks):
        return " " if n_clicks else dash.no_update

    # Show the responding reminder based on the value the user chooses.
    # (for the copyright) The follwings are from Ubereats:
    # 1: Very disappointing. What went wrong?
    # 2: Pretty bad. What went wrong?
    # 3: Just Average. What went wrong?
    # 4: Pretty good, but what could be better?
    # 5: Excellent! What did you enjoy?
    @app.callback(Output('rating-remind', 'children'),
                  [Input('rating-score', 'value')]
                  )
    def showRatingRemind(rating_score):
        if rating_score == 1:
            return html.H6("Very disappointing. What went wrong?")
        if rating_score == 2:
            return html.H6("Pretty bad. What went wrong?")
        if rating_score == 3:
            return html.H6("Just Average. What went wrong?")
        if rating_score == 4:
            return html.H6("Pretty good, but what could be better?")
        if rating_score == 5:
            return html.H6("Excellent! What did you enjoy?")
        else:
            return html.H6("Please rate, it really helps.")
