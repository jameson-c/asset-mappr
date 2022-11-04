"""
File: catSummary_Planner_cb.py
Author: Mihir Bhaskar, Anna Wang

Desc: This file creates the callback that generates the category summary bar graphs in the planner dashboard
      
This is linked to the showMap_Planner.py feature in presentation

Input: 
    app: an initialized dash app
    master_categories: a list of the unique possible set of category values
    asset_categories: data frame with assets and their catagories (in separate df because 1 asset can have many cats)
    missing_assets: data frame with suggestion assets from community members
    rating_score: data frame of the ratings table
Output: 
    Callbacks relating to the showMap_Planner feature
     
"""
from matplotlib.pyplot import ylabel
import pandas as pd  # (version 0.24.2)
import dash  # (version 1.0.0)
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import numpy as np

import plotly.express as px

# the readDB function does the SQL interaction
from AssetMappr.database.readDB import readDB

def catSummary_Planner_cb(app):
    
    # Callback which creates the bar chart by category based on the selected input statistic desired
    @app.callback(
        Output('bar-chart-for-planner', 'figure'),
        Input('choose-the-stat', 'value'),
        # Retrieves the relevant community's data from the dcc.Store object
        [Input('asset-categories-cnm', 'data')],
        [Input('missing-assets-planner-view', 'data')],
        [Input('rating-score-planner-view', 'data')],
        
        )
    def showChart(stat_type,asset_categories,missing_assets,rating_score):
        # Transform the JSON format data from the dcc.Store back into data frames
        asset_categories = pd.read_json(asset_categories, orient='split')
        missing_assets = pd.read_json(missing_assets, orient='split')
        rating_score = pd.read_json(rating_score, orient='split')
            
        # Counts by category for existing assetse
        existing_cat_counts = asset_categories.groupby('category').count()

        # Getting the average rating and number of ratings for each asset
        avg_rating_assets = rating_score.groupby('asset_id').agg(avg_asset_rating=('rating_scale', np.mean),
                                                                num_ratings=('staged_rating_id', np.count_nonzero))

        # Merging this ratings data to see the category each asset belongs to
        cat_ratings = pd.merge(asset_categories, avg_rating_assets, on='asset_id')

        # Aggregating the data again at a category level - taking an average of the average ratings across assets,
        # summing the total ratings observed for a category, and getting the unique assets over which those ratings were observed

        cat_ratings = cat_ratings.groupby('category').agg(avg_cat_rating=('avg_asset_rating', np.mean),
                                                        tot_ratings=(
                                                            'num_ratings', 'sum'),
                                                        unique_assets=('asset_id', pd.Series.nunique))

        # Counts by primary category for missing/suggested assets
        missing_cat_counts = missing_assets.groupby('primary_category').agg(
            count=('suggestion_id', pd.Series.nunique))      
            


        # Barchart to show count of existing assets by category
        if stat_type == 'count_number':
            barchart = px.bar(
                existing_cat_counts,
                x=existing_cat_counts['asset_id'],
                opacity=0.9,
                barmode='group',

                labels={"asset_id": "Number of assets"},
                title="Number of existing assets by category",
                orientation='h')
            barchart.update_layout(
                yaxis={'categoryorder': 'total ascending'}, yaxis_title=None)

        # Barchart to show the average rating across all assets in each category
        elif stat_type == 'rating_avg':
            barchart = px.bar(
                cat_ratings,
                x=round(cat_ratings['avg_cat_rating'], 2),
                # color="INDEX_NAME",
                opacity=0.9,
                barmode='group',
                custom_data=[cat_ratings['tot_ratings'],cat_ratings['unique_assets']],
                # Average score: (), from () ratings across () assets
                labels={
                    "avg_cat_rating": "Average rating () from () ratings across () assets"},
                title="Average asset ratings by category",
                orientation='h')

            barchart.update_traces(
                hovertemplate='Average rating %{x} from %{customdata[0]} ratings across %{customdata[1]} assets <extra></extra>')

            barchart.update_layout(
                yaxis={'categoryorder': 'total ascending'}, yaxis_title=None, xaxis_title='Average rating')

        # Barchart to show the count of missing assets for each category
        else:
            barchart = px.bar(
                missing_cat_counts,
                x=missing_cat_counts['count'],
                # color="INDEX_NAME",
                opacity=0.9,
                barmode='group',

                labels={"count": "Number of suggested missing assets"},
                title="Number of suggested 'missing' assets by category",

                orientation='h')
            barchart.update_layout(
                yaxis={'categoryorder': 'total ascending'}, yaxis_title=None)

        return barchart
