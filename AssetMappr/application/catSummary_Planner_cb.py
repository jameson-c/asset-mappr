import pandas as pd  # (version 0.24.2)
import datetime as dt
import dash  # (version 1.0.0)
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import numpy as np

import plotly  # (version 4.4.1)
import plotly.express as px


def catSummary_Planner_cb(app, master_categories, asset_categories, missing_assets, rating_score):
    
    # Counts by category
    existing_cat_counts = asset_categories.groupby('category').count()
        
    # Getting the average rating across all assets that were rated in the category
    avg_rating_assets = rating_score.groupby('asset_id').agg(avg_asset_rating= ('rating_scale', np.mean),
                                                             num_ratings = ('staged_rating_id', np.count_nonzero))
    
    cat_ratings = pd.merge(asset_categories, avg_rating_assets, on='asset_id')
    
    
    cat_ratings = cat_ratings.groupby('category').agg(avg_cat_rating = ('avg_asset_rating', np.mean),
                                                      tot_ratings = ('num_ratings', 'sum'),
                                                      unique_assets = ('asset_id', pd.Series.nunique))
    
    missing_cat_counts = missing_assets.groupby('primary_category').agg(count = ('suggestion_id', pd.Series.nunique))
    

    @app.callback(
        Output(component_id='bar-chart-for-planner',
               component_property='figure'),
        Input('choose-the-stat', 'value'))
    def showChart(stat_type):
        
        # Declaring the above processed datasets as nonlocals so this nested function can access
        nonlocal existing_cat_counts, cat_ratings, missing_cat_counts
        
        if stat_type == 'count_number':
            barchart = px.bar(
                existing_cat_counts,
                x=existing_cat_counts['asset_id'],
                opacity=0.9,
                barmode='group',
                
                labels={"asset_id": "Count"},
                title="Number of existing assets by category",
                
                orientation='h')
            barchart.update_layout(yaxis={'categoryorder': 'total ascending'})
        
        elif stat_type == 'rating_avg':
            barchart = px.bar(
                cat_ratings,
                x=cat_ratings['avg_cat_rating'],
                # color="INDEX_NAME",
                opacity=0.9,
                barmode='group',
                
                labels={"avg_cat_rating": "Average rating across all assets in category"},
                title="Average asset ratings by category",
                
                orientation='h')
            barchart.update_layout(yaxis={'categoryorder': 'total ascending'})
            
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
            barchart.update_layout(yaxis={'categoryorder': 'total ascending'})
            

        return barchart