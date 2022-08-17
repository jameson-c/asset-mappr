"""
File: topAssets_Planner.py
Author: Mihir Bhaskar, Anna Wang

Desc: This file returns an HTML Div with the top/bottom assets by ratings

This function has no associated callback, because there is no user interactivity. It just
processes the data read in by the app initially, on ratings, and displays the output.

Inputs:
    - df: data frame of the main assets table
    - rating_score: data frame of the ratings table (NOTE: CURRENTLY THIS IS STAGED RATINGS - need to change code accordingly)
    - rating_values: data frame of the mapping from ratings to 'value tags' associated with that rating

Output:
    - HTML Div, called in makeLayout()
"""
from curses.panel import bottom_panel
import dash_bootstrap_components as dbc
from dash import html
import pandas as pd
import numpy as np

import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

import dash_html_components as html


def topAssets_cb(app):

    # Callback which creates the bar chart by category based on the selected input statistic desired
    @app.callback(
        Output('top-assets', 'children'),
        # Retrieves the relevant community's data from the dcc.Store object
        [Input('assets-df', 'data')],
        [Input('rating-score-planner-view', 'data')],
        [Input('rating-value-planner-view', 'data')]
    )
    def topAssets_Planner(df, rating_score, rating_values):
        # retrieve data from json dcc.store
        df = pd.read_json(df, orient='split')
        rating_score = pd.read_json(rating_score, orient='split')
        rating_values = pd.read_json(rating_values, orient='split')

        ### DATA PROCESSING ###
        # Keep only the fields needed in the main assets table
        df = df[['asset_id', 'asset_name']]

        # Step 1: get the 'most common' value tag for a given asset
        # Merging rating-values table with rating-score to get the asset_id
        rating_values = pd.merge(rating_values, rating_score[[
            'staged_rating_id', 'asset_id']], on='staged_rating_id')

        # Merge the rating-values table with the main assets data frame
        asset_values = pd.merge(df, rating_values, on='asset_id')

        # Aggregate this table by asset_id to get the most frequently chosen value for each asset
        asset_values = asset_values.groupby('asset_id').agg(
            most_common_value=('value', lambda x: x.value_counts().index[0]))

        # Pull asset_id out of the index for later use in merging (during the merge, asset_id gets pushed into the index)
        asset_values = asset_values.reset_index()

        # Step 2: get info about the rating score from the ratings table

        # Aggregate ratings table by asset_id, to get the average rating and the number of ratings for each asset
        avg_rating_assets = rating_score.groupby('asset_id').agg(avg_asset_rating=('rating_scale', np.mean),
                                                                 num_ratings=('staged_rating_id', np.count_nonzero))

        # pull asset_id out of index fo rlater use in merging
        avg_rating_assets = avg_rating_assets.reset_index()

        ## Step 3: extract one comment at random from the set of comments associated with an asset's ratings, to display ##

        comments_df = rating_score[['asset_id', 'comments']]
        comments_df = comments_df.dropna(
            subset=['comments'])  # drop missing comments
        # drop empty comments that are basically missing but not NA
        comments_df = comments_df[~comments_df['comments'].isin(['', ' '])]

        # Randomly sample one comment per asset_id
        comments_df = comments_df.groupby('asset_id').apply(
            lambda x: x.sample(1)).reset_index(drop=True)

        ## Step 4: merging all the data together into one data frame ##

        # Using left joins here because not all assets may have all of the rating information. E.g. some assets may have
        # ratings, but no comments. Using left join with the main assets df table makes sure we don't drop any assets because of this.
        # comments_df may be empty. Setting the condition for that.

        df = pd.merge(df, asset_values, on='asset_id', how='left')
        df = pd.merge(df, avg_rating_assets, on='asset_id', how='left')
        
        ## Step 5: Selecting assets with at least five ratings so the ratings average is reliable ##
        # drop assets with no ratings at all
        df = df.dropna(subset=['avg_asset_rating'])
        print(df)
        print(df[df['num_ratings'] >= 5])
        # keep if there are at least 5 ratings for the asset
        if df[df['num_ratings'] >= 5].empty == False:
            ## comments_df may be empty
            if comments_df.empty == False:
                df = pd.merge(df, comments_df, on='asset_id', how='left')
                df = df[df['num_ratings'] >= 5]
                # Sort values from descending to ascending, so the 'worst' assets are first rows, best are bottom rows
                df = df.sort_values(['avg_asset_rating'])
                #setting the varibles which will be used in the return
                topAsset_1_Name = df['asset_name'].iloc[-1]
                topAsset_1_Value = df['most_common_value'].iloc[-1]
                topAsset_1_Comment = df['comments'].iloc[-1]
                topAsset_1_AvgScore = df['avg_asset_rating'].iloc[-1]
                topAsset_1_NumRating =  df['num_ratings'].iloc[-1]
                
                topAsset_2_Name = df['asset_name'].iloc[-2]
                topAsset_2_Value = df['most_common_value'].iloc[-2]
                topAsset_2_Comment = df['comments'].iloc[-2]
                topAsset_2_AvgScore = df['avg_asset_rating'].iloc[-2]
                topAsset_2_NumRating =  df['num_ratings'].iloc[-2]
                
                bottom_1_Name = df['asset_name'].iloc[0]
                bottom_1_Value = df['most_common_value'].iloc[0]
                bottom_1_Comment = df['comments'].iloc[0]
                bottom_1_AvgScore = df['avg_asset_rating'].iloc[0]
                bottom_1_NumRating =  df['num_ratings'].iloc[0]
                
                bottom_2_Name = df['asset_name'].iloc[1]
                bottom_2_Value = df['most_common_value'].iloc[1]
                bottom_2_Comment = df['comments'].iloc[1]
                bottom_2_AvgScore = df['avg_asset_rating'].iloc[1]
                bottom_2_NumRating =  df['num_ratings'].iloc[1] 
            else:
                #setting the varibles which will be used in the return when comments is empty
                topAsset_1_Name = df['asset_name'].iloc[-1]
                topAsset_1_Value = df['most_common_value'].iloc[-1]
                topAsset_1_Comment = 'No comments yet'
                topAsset_1_AvgScore = df['avg_asset_rating'].iloc[-1]
                topAsset_1_NumRating =  df['num_ratings'].iloc[-1]
                
                topAsset_2_Name = df['asset_name'].iloc[-2]
                topAsset_2_Value = df['most_common_value'].iloc[-2]
                topAsset_2_Comment ='No comments yet'
                topAsset_2_AvgScore = df['avg_asset_rating'].iloc[-2]
                topAsset_2_NumRating =  df['num_ratings'].iloc[-2]
                
                bottom_1_Name = df['asset_name'].iloc[0]
                bottom_1_Value = df['most_common_value'].iloc[0]
                bottom_1_Comment ='No comments yet'
                bottom_1_AvgScore = df['avg_asset_rating'].iloc[0]
                bottom_1_NumRating =  df['num_ratings'].iloc[0]
                
                bottom_2_Name = df['asset_name'].iloc[1]
                bottom_2_Value = df['most_common_value'].iloc[1]
                bottom_2_Comment = 'No comments yet'
                bottom_2_AvgScore = df['avg_asset_rating'].iloc[1]
                bottom_2_NumRating =  df['num_ratings'].iloc[1] 
                 
                ### CREATING THE ACTUAL DISPLAY COMPONENTS ###
                
            return html.Div([

                # Header for the 'top' 2 assets section

                html.H5('Top assets by rating', style={
                        'font-size': '23px', 'font-weight': 'bold', 'color': 'darkolivegreen', 'margin-left': '18px'}),

                # CardGroup groups the two display cards together, so they're the same height/appear in the same row
                dbc.CardGroup([

                    # Top asset number 1, with highest rating: the last row of sorted df created above
                    dbc.Card([

                        dbc.CardHeader(topAsset_1_Name, style={
                            'font-size': '14px', 'font-weight': 'bold'}),

                        dbc.CardBody([

                            # Badge that displays the most common value. 'Success' and the classname are standard
                            # badge formats selected from the dbc documentation; basically it makes a green 'pill'-shaped badge
                            dbc.Badge(topAsset_1_Value, pill=True, color='success',
                                    className="me-1"),

                            html.Br(),

                            # Displaying the randomly chosen comment in quotation marks
                            html.P([' "{}" '.format(topAsset_1_Comment)],
                                style={'margin-top': '10px'}),

                        ]),

                        # Showing the average rating and total number of ratings
                        dbc.CardFooter(['Average rating: {:.2f} out of 5 (from {} ratings)'.format(topAsset_1_AvgScore,
                                                                                                topAsset_1_NumRating)
                                        ]),

                    ]),

                    # Top Asset Number 2 (the second-from-bottom row in DF)
                    # Same structure followed as above
                    dbc.Card([

                        dbc.CardHeader(topAsset_2_Name, style={
                            'font-size': '14px', 'font-weight': 'bold'}),

                        dbc.CardBody([

                            dbc.Badge(topAsset_2_Value, pill=True, color='success',
                                    className="me-1"),

                            html.Br(),

                            html.P('''"{}"'''.format(
                                topAsset_2_Comment), style={'margin-top': '10px'}),

                        ]),

                        dbc.CardFooter(['Average rating: {:.2f} out of 5 (from {} ratings)'.format(topAsset_2_AvgScore,
                                                                                                int(topAsset_2_NumRating))
                                        ]),

                    ]),

                ]),
                html.Br(),

                html.H5('Bottom assets by rating', style={
                        'font-size': '23px', 'font-weight': 'bold', 'color': 'maroon', 'margin-left': '18px'}),

                # Cardgroup for bottom 2 assets - same structure followed as for top assets
                dbc.CardGroup([

                    dbc.Card(className="card", children=[

                        # The worst asset is the first row of df, hence iloc[0]
                        dbc.CardHeader(bottom_1_Name, style={
                            'font-size': '14px', 'font-weight': 'bold'}),

                        dbc.CardBody([

                            # Color changed to 'danger', to format it as red background - white text
                            dbc.Badge(bottom_1_Value, pill=True, color='danger',
                                    className="me-1"),

                            html.Br(),

                            html.P('''"{}"'''.format(bottom_1_Comment), style={
                                'margin-top': '18px'}),

                        ]),

                        dbc.CardFooter(['Average rating: {:.2f} out of 5 (from {} ratings)'.format(bottom_1_AvgScore,
                                                                                                int(bottom_1_NumRating))
                                        ]),

                    ]),

                    # Card for second-worst asset (second row in the dataset)
                    dbc.Card(className="card", children=[

                        dbc.CardHeader(bottom_2_Name, style={
                            'font-size': '14px', 'font-weight': 'bold'}),

                        dbc.CardBody([

                            dbc.Badge(bottom_2_Value, pill=True, color='danger',
                                    className="me-1"),

                            html.Br(),


                            html.P('''"{}"'''.format(bottom_2_Comment), style={
                                'margin-top': '10px'}),

                        ]),

                        dbc.CardFooter(['Average rating: {:.2f} out of 5 (from {} ratings)'.format(bottom_2_AvgScore,
                                                                                                int(bottom_2_NumRating))]),

                    ]),

                ]),

            ])
        else:
            return html.H5('We don\'t have enough data to show which are the top assets or bottom assets.',id='no-enough-ratings-top-assets')
