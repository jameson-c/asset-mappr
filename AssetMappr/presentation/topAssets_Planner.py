"""
File: topAssets_Planner.py
Author: Mihir Bhaskar

Desc: This file returns an HTML Div with the top/bottom assets by ratings

The main map is created in showMap_Planner_cb in the application folder

Input

Output:
    - HTML Div, called in makeLayout()
"""
import dash_bootstrap_components as dbc
from dash import html
import pandas as pd
import numpy as np

def topAssets_Planner(df, rating_score, rating_values):
    
    # Data processing to get the top and bottom assets
    
    # Keep only what's needed in df
    df = df[['asset_id', 'asset_name']]
    
    # Add asset_id to rating values table 
    rating_values = pd.merge(rating_values, rating_score[['staged_rating_id', 'asset_id']], on='staged_rating_id')
    
    # Merge the rating values table with the 
    asset_values = pd.merge(df, rating_values, on='asset_id')
    
    # Aggregate this table by asset_id to get the top value for each asset
    asset_values = asset_values.groupby('asset_id').agg(most_common_value = ('value', lambda x: x.value_counts().index[0]))
    
    asset_values = asset_values.reset_index() # pull asset_id out of the index for later use in merging
    
    # Collapse ratings table down to one observation per asset, which is the average rating
    avg_rating_assets = rating_score.groupby('asset_id').agg(avg_asset_rating= ('rating_scale', np.mean),
                                                             num_ratings = ('staged_rating_id', np.count_nonzero))
    avg_rating_assets = avg_rating_assets.reset_index() # pull asset_id out of index fo rlater use in merging

    # Extract one nonmissing comment out for each asset
    comments_df = rating_score[['asset_id', 'comments']]
    comments_df = comments_df.dropna(subset=['comments'])
    comments_df = comments_df[~comments_df['comments'].isin(['', ' '])]   
    
    # Randomly sample one comment per asset_id
    comments_df = comments_df.groupby('asset_id').apply(lambda x: x.sample(1)).reset_index(drop=True)
    
    # Merging all the useful data together
    df = pd.merge(df, asset_values, on='asset_id', how='left')
    df = pd.merge(df, avg_rating_assets, on='asset_id', how='left')
    df = pd.merge(df, comments_df, on='asset_id', how='left')
    
    # Selecting assets with at least five ratings and sorting
    df = df.dropna(subset=['avg_asset_rating'])
    df = df[df['num_ratings'] >= 5]
    df = df.sort_values(['avg_asset_rating'])
    
    return html.Div([
        
        html.H5('Top assets by rating'),
        
        dbc.CardGroup([
            
            # Top asset
            dbc.Card([
                
                dbc.CardHeader(df['asset_name'].iloc[-1]), # Getting the name of the best asset by picking the last observation in sorted df
                
                dbc.CardBody([
                    
                    dbc.Badge(df['most_common_value'].iloc[-1], pill=True, color='success', 
                              className="me-1"),
                    
                    html.Br(),
                                        
                    html.P('''"{}"'''.format(df['comments'].iloc[-1])),
                    
                    ]),
                
                dbc.CardFooter(['Average rating: {:.2f} out of 5 (from {} ratings)'.format(df['avg_asset_rating'].iloc[-1],
                                                                                            df['num_ratings'].iloc[-1])
                                ]),
                
                ]),
            
            dbc.Card([
                
                dbc.CardHeader(df['asset_name'].iloc[-2]),
                
                dbc.CardBody([
                    
                    dbc.Badge(df['most_common_value'].iloc[-2], pill=True, color='success', 
                              className="me-1"),
                    
                    html.Br(),
                                        
                    html.P('''"{}"'''.format(df['comments'].iloc[-2])),
                    
                    ]),
                
                dbc.CardFooter(['Average rating: {:.2f} out of 5 (from {} ratings)'.format(df['avg_asset_rating'].iloc[-2],
                                                                                            df['num_ratings'].iloc[-2])
                                ]),
                
                ]),           
            
            
            ]),
        
        html.H5('Bottom assets by rating'),
        
        dbc.CardGroup([
            
            dbc.Card([
                
                dbc.CardHeader(df['asset_name'].iloc[0]),
                
                dbc.CardBody([
                    
                    dbc.Badge(df['most_common_value'].iloc[0], pill=True, color='danger', 
                              className="me-1"),
                    
                    html.Br(),
                    
                    html.P('''"{}"'''.format(df['comments'].iloc[0])),
                    
                    ]),
                
                dbc.CardFooter(['Average rating: {:.2f} out of 5 (from {} ratings)'.format(df['avg_asset_rating'].iloc[0],
                                                                                            df['num_ratings'].iloc[0])
                               ]),
                
                ]),
            
            dbc.Card([
                
                dbc.CardHeader(df['asset_name'].iloc[1]),
                
                dbc.CardBody([
                    
                    dbc.Badge(df['most_common_value'].iloc[1], pill=True, color='danger', 
                              className="me-1"),
                    
                    html.Br(),
                    
                    
                    html.P('''"{}"'''.format(df['comments'].iloc[1])),
                    
                    ]),
                
                dbc.CardFooter(['Average rating: {:.2f} out of 5 (from {} ratings)'.format(df['avg_asset_rating'].iloc[1],
                                                                                            df['num_ratings'].iloc[1])
                                ]),
                
                ]),           
            
            ]),  
        
        ])
        


