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
from dash import dcc

from AssetMappr.database.submitRating_db import submitRating_db


def submitRating_cb(app, tagList_pos, tagList_neg):
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

            # Write the rating information to the staged ratings table in the DB
            submitRating_db(asset_id, rating_score, rating_comments, value_tag)
            return dbc.Alert('Your review has been submitted - Thanks for sharing! ', dismissable=True, color='success')

    # Show the label: "How do you feel about XXXX(asset name)?"
    @app.callback(Output('HowDoYouFeel', 'children'),
                  Input('graph', 'clickData')
                  )
    def review_label(clickData):
        if clickData == None:
            return 'After clicking the asset, you can rate it.'
        else:
            asset_name = clickData['points'][0]['customdata'][0]
            return 'How do you feel about {}?'.format(asset_name)

    # clear after submitting
    @app.callback(Output('rating-comments', 'value'),
                  Output('rating-score', 'value'),
                Input('submit-rating-button', 'n_clicks')
                )
    def clear_persistence(n_clicks):
        return " ",1 if n_clicks else dash.no_update

    # Show the responding reminder based on the value the user chooses.
    # (for the copyright) The follwings are from Ubereats:
    # 1: Very disappointing. What went wrong?
    # 2: Pretty bad. What went wrong?
    # 3: Just Average. What went wrong?
    # 4: Pretty good, but what could be better?
    # 5: Excellent! What did you enjoy?
    @app.callback(Output('rating-remind', 'children'),
                  [Input('rating-score', 'value'),
                   Input('submit-rating-button', 'n_clicks')]
                  )
    def showRatingRemind(rating_score,n_clicks):
        if n_clicks >0:
            return html.H6("Please rate, it really helps.")
        else:
            if rating_score == 1:
                return html.H6("Bad or harmful for the community")
            if rating_score == 2:
                return html.H6("Not very useful for the community")
            if rating_score == 3:
                return html.H6("Neutral - no strong feelings")
            if rating_score == 4:
                return html.H6("Good for the community, some areas for improvement")
            if rating_score == 5:
                return html.H6("Extremely important/valuable for the community")
            else:
                return html.H6("Please rate, it really helps.")

    # change the value tag options based on the rating score
    @app.callback([Output('value-tag', 'options'),
                   Output('value-tag', 'value')],
                  Input('rating-score', 'value'),
                  Input('submit-rating-button', 'n_clicks')
                  )
    def showValue(rating_score,n_clicks):     
        if n_clicks > 0:
            return  [{'label': i, 'value': i} for i in tagList_pos],None
        else:
            # default(before clicking the asset)
            if rating_score == None:
                return [{'label': i, 'value': i} for i in tagList_pos], None
            elif rating_score <= 3:
                return [{'label': i, 'value': i} for i in tagList_neg], None
            else:
                return [{'label': i, 'value': i} for i in tagList_pos], None
            
   
            