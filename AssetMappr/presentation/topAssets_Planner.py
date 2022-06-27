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
import dash_bootstrap_components as dbc
from dash import html
import pandas as pd
import numpy as np


def topAssets_Planner(df, rating_score, rating_values):

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

    df = pd.merge(df, asset_values, on='asset_id', how='left')
    df = pd.merge(df, avg_rating_assets, on='asset_id', how='left')
    df = pd.merge(df, comments_df, on='asset_id', how='left')

    ## Step 5: Selecting assets with at least five ratings so the ratings average is reliable ##
    # drop assets with no ratings at all
    df = df.dropna(subset=['avg_asset_rating'])
    # keep if there are at least 5 ratings for the asset
    df = df[df['num_ratings'] >= 5]
    # Sort values from descending to ascending, so the 'worst' assets are first rows, best are bottom rows
    df = df.sort_values(['avg_asset_rating'])

    ### CREATING THE ACTUAL DISPLAY COMPONENTS ###

    return html.Div([

        # Header for the 'top' 2 assets section

        html.H5('Top assets by rating \U0001F603', style={
                'font-size': '23px', 'font-weight': 'bold', 'color': 'darkolivegreen'}),

        # CardGroup groups the two display cards together, so they're the same height/appear in the same row
        dbc.CardGroup([

            # Top asset number 1, with highest rating: the last row of sorted df created above
            dbc.Card([

                dbc.CardHeader(df['asset_name'].iloc[-1], style={
                               'font-size': '14px', 'font-weight': 'bold'}),

                dbc.CardBody([

                    # Badge that displays the most common value. 'Success' and the classname are standard
                    # badge formats selected from the dbc documentation; basically it makes a green 'pill'-shaped badge
                    dbc.Badge(df['most_common_value'].iloc[-1], pill=True, color='success',
                              className="me-1"),

                    html.Br(),

                    # Displaying the randomly chosen comment in quotation marks
                    html.P(' "{}" '.format(df['comments'].iloc[-1])),

                ]),

                # Showing the average rating and total number of ratings
                dbc.CardFooter(['Average rating: {:.2f} out of 5 (from {} ratings)'.format(df['avg_asset_rating'].iloc[-1],
                                                                                           int(df['num_ratings'].iloc[-1]))
                                ]),

            ]),

            # Top Asset Number 2 (the second-from-bottom row in DF)
            # Same structure followed as above
            dbc.Card([

                dbc.CardHeader(df['asset_name'].iloc[-2], style={
                               'font-size': '14px', 'font-weight': 'bold'}),

                dbc.CardBody([

                    dbc.Badge(df['most_common_value'].iloc[-2], pill=True, color='success',
                              className="me-1"),

                    html.Br(),

                    html.P('''"{}"'''.format(df['comments'].iloc[-2])),

                ]),

                dbc.CardFooter(['Average rating: {:.2f} out of 5 (from {} ratings)'.format(df['avg_asset_rating'].iloc[-2],
                                                                                           int(df['num_ratings'].iloc[-2]))
                                ]),

            ]),


        ]),
        html.Br(),

        html.H5('Bottom assets by rating \U0001F928', style={
                'font-size': '23px', 'font-weight': 'bold', 'color': 'maroon'}),

        # Cardgroup for bottom 2 assets - same structure followed as for top assets
        dbc.CardGroup([

            dbc.Card(className="card", children=[

                # The worst asset is the first row of df, hence iloc[0]
                dbc.CardHeader(df['asset_name'].iloc[0], style={
                               'font-size': '14px', 'font-weight': 'bold'}),

                dbc.CardBody([

                    # Color changed to 'danger', to format it as red background - white text
                    dbc.Badge(df['most_common_value'].iloc[0], pill=True, color='danger',
                              className="me-1"),

                    html.Br(),

                    html.P('''"{}"'''.format(df['comments'].iloc[0])),

                ]),

                dbc.CardFooter(['Average rating: {:.2f} out of 5 (from {} ratings)'.format(df['avg_asset_rating'].iloc[0],
                                                                                           int(df['num_ratings'].iloc[0]))
                                ]),

            ]),

            # Card for second-worst asset (second row in the dataset)
            dbc.Card(className="card", children=[

                dbc.CardHeader(df['asset_name'].iloc[1], style={
                               'font-size': '14px', 'font-weight': 'bold'}),

                dbc.CardBody([

                    dbc.Badge(df['most_common_value'].iloc[1], pill=True, color='danger',
                              className="me-1"),

                    html.Br(),


                    html.P('''"{}"'''.format(df['comments'].iloc[1])),

                ]),

                dbc.CardFooter(['Average rating: {:.2f} out of 5 (from {} ratings)'.format(df['avg_asset_rating'].iloc[1],
                                                                                           int(df['num_ratings'].iloc[1]))
                                ]),

            ]),

        ]),

    ])
