"""
File: tableDownload_Planner_cb.py
Author: Mihir Bhaskar

Desc: This file creates the callback that generates the table display and download option in the planner view
      
This is linked to the tableDownload_Planner.py feature in presentation

Input: 
    app: an initialized dash app
    df: main data frame with assets to be displayed
    asset_categories: data frame with assets and their catagories (in separate df because 1 asset can have many cats)
    missing_assets: data frame with suggestion assets from community members
    rating_score: data frame of the ratings table
Output: 
    Callbacks relating to the showMap_Planner feature
     
"""
from dash.dependencies import Input, Output, State
from dash import html, dcc
import pandas as pd
import numpy as np
from dash import dash_table


def tableDownload_Planner_cb(app, df, asset_categories, missing_assets, rating_score, rating_values):

    # Processing data into the type of table we want
    df = df[['asset_id', 'asset_name', 'description', 'address', 'website']]
    
    # Making asset_categories data wide to it can be merged uniquely with df
    
    # Starting a counter variable in asset categories so that I can name category_1, category_2, etc.
    asset_categories['counter'] = asset_categories.groupby('asset_id').cumcount() + 1
    asset_categories['counter'] = asset_categories['counter'].apply(str)
    asset_categories['counter'] = 'category_' + asset_categories['counter']
    
    asset_categories = asset_categories.pivot(index='asset_id', columns='counter', values='category')
    
    df = pd.merge(df, asset_categories, on='asset_id')
    
    # Add asset_id to rating values table 
    rating_values = pd.merge(rating_values, rating_score[['staged_rating_id', 'asset_id']], on='staged_rating_id')
    
    # Merge the rating values table with the 
    asset_values = pd.merge(df, rating_values, on='asset_id')
    
    # Aggregate this table by asset_id to get the top value for each asset
    asset_values = asset_values.groupby('asset_id').agg(most_common_rated_value = ('value', lambda x: x.value_counts().index[0]))
    
    asset_values = asset_values.reset_index() # pull asset_id out of the index for later use in merging
    
    df = pd.merge(df, asset_values, on='asset_id', how='left')
    
    # Collapse ratings table down to one observation per asset, which is the average rating
    avg_rating_assets = rating_score.groupby('asset_id').agg(avg_asset_rating= ('rating_scale', np.mean),
                                                             num_ratings = ('staged_rating_id', np.count_nonzero))
    avg_rating_assets = avg_rating_assets.reset_index() # pull asset_id out of index fo rlater use in merging
    
    df = pd.merge(df, avg_rating_assets, on='asset_id', how='left')

    # Combine comments for the asset from the ratings
    comments_df = rating_score[['asset_id', 'comments']]
    comments_df = comments_df.dropna(subset=['comments'])
    comments_df = comments_df[~comments_df['comments'].isin(['', ' '])]   
    
    # Join all the comments together
    comments_df['all_comments'] = comments_df.groupby('asset_id')['comments'].transform(lambda x: ' | '.join(x))
    comments_df.drop_duplicates('asset_id')
    
    # Merge this onto the overall df
    df = pd.merge(df, comments_df[['asset_id', 'all_comments']], on='asset_id', how='left')
    
    # Keep missing_df ready
    missing_df = missing_assets[['missing_asset_name', 'description', 'primary_category', 'address', 'justification', 'generated_timestamp']]
    
    
    # This callback receives input on which type of assets the user has selected 
    # And outputs the table object
    @app.callback(Output('data-table', 'children'),
                  Input('choose-the-table-source', 'value'),
                  )
    def update_table(type_of_assets):
        
        nonlocal df, missing_df
        
        if type_of_assets == 'Existing Assets':
            tmpdta = df.to_dict('rows')
            tmpcols = [{"name": i, "id": i,} for i in (df.columns)]
            
 
        else:
            tmpdta = missing_df.to_dict('rows')
            tmpcols = [{"name": i, "id": i,} for i in (missing_df.columns)]
            
        # Return a well-formatted dash table
        return dash_table.DataTable(data = tmpdta, columns = tmpcols)
        
    # This callback interacts with the download button to download the data as an Excel file
    @app.callback(
        Output('download-dataframe-xlsx', 'data'),
        [Input('download_button', 'n_clicks')],
        [State('choose-the-table-source', 'value')],
        prevent_initial_call = True,
        )
    def download_function(n_clicks, type_of_assets):
        
        nonlocal df, missing_df
        
        if n_clicks:
        
            if type_of_assets == 'Existing Assets':
                return dcc.send_data_frame(df.to_excel, "existing_assets.xlsx", sheet_name='Existing Assets')
            else:
                return dcc.send_data_frame(missing_df.to_excel, "missing_asset_suggestions.xlsx", sheet_name='Missing Suggested Assets')