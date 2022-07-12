"""
File: showMap_Planner_cb.py
Author: Anna Wang

Desc: This file creates the callback that generates the asset map display for planner view
      
This is linked to the showMap_Planner.py feature in presentation

Input: 
    app: an initialized dash app
    df: main data frame with assets to be displayed
    asset_categories: data frame with assets and their catagories (in separate df because 1 asset can have many cats)
    missing_assets: data frame with suggestion assets from community members
    rating_score: data frame of the ratings table
Output: 
    Callbacks relating to the showMap_Planner feature
     
"""
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np


def showMap_Planner_cb(app, df, asset_categories, missing_assets, rating_score):
    

    # This callback receives input on which categories the user has selected 
    # And outputs the map object
    @app.callback(Output('graph-for-planner', 'figure'),
                  [Input('choose-the-source', 'value')],
                  [Input('map-type', 'value')],
                # Retrieves the relevant community's data from the dcc.Store object
                [Input('assets-df', 'data')],
                [Input('asset-categories-cnm', 'data')],
                [Input('missing-assets-planner-view', 'data')],
                [Input('rating-score-planner-view', 'data')],
                [Input('selected-community-info', 'data')],)
    def update_figure(choose_the_source, map_type,df_cnm,asset_categories,missing_assets,rating_score,selected_community):
        # Transform the JSON format data from the dcc.Store back into data frames
        df_cnm = pd.read_json(df_cnm, orient='split')
        asset_categories = pd.read_json(asset_categories, orient='split')
        missing_assets = pd.read_json(missing_assets, orient='split')
        rating_score = pd.read_json(rating_score, orient='split')
        selected_community = pd.read_json(selected_community, orient='split')
        
        # Merge the assets and asset-category mappings into a single df
        map_df = pd.merge(df, asset_categories, on='asset_id')
        
        
        # Add the average rating score for the asset to the data frame
        avg_rating = rating_score.groupby(
            'asset_id').agg({'rating_scale': [np.mean]})
        pd.set_option('display.max_columns', None)
        map_df = pd.merge(map_df, avg_rating,on='asset_id', how='left')
        map_df['avg_score'] = map_df.iloc[:,-1]
        map_df = pd.merge(map_df,rating_score,on='asset_id',how='left')



        # We should change this part when the categories are changed. Becuase each category has one symbol, it is a one on one thing, we have to manually choose the symbol for each category.
        categoryList = ["Sports and recreation", "Culture and history", "Education and workforce development",
                        "Healthcare", "Housing", "Places of worship", "Community service and assistance", "Transport and infrastructure",
                        "Food access", "Nature and parks", "Libraries", "Economic development opportunities", "Local business and economy"]
 
 
        #These symbols are from: https://labs.mapbox.com/maki-icons
        symbolList = ['american-football', 'museum', 'school', 'hospital-JP',
                      'lodging',
                      'place-of-worship',
                      'toilet',
                      'bus',
                      'grocery',
                      'park',
                      'library',
                      'circle-stroked',
                      'bank']

        # Zip the categoryList and symbolList. Each category has their different symbol.
        for item in zip(categoryList, symbolList):
            map_df.loc[map_df['category'] == item[0],
                       'symbolBasedCategory'] = item[1]
        
        # Setting mapbox access token (this is for accessing their base maps)
        mapbox_access_token = 'pk.eyJ1IjoicWl3YW5nYWFhIiwiYSI6ImNremtyNmxkNzR5aGwyb25mOWxocmxvOGoifQ.7ELp2wgswTdQZS_RsnW1PA'
        
        
        # Get the community lat-long to center on (from the selected community info)
        community_center_lat = float(selected_community['latitude'])
        community_center_lon = float(selected_community['longitude'])
        
        # Setting the layout for the map (same regardless of the options chosen)
        layout = go.Layout(
                uirevision='foo',  # preserves state of figure/map after callback activated
                clickmode='event+select',
                hovermode='closest',
                hoverdistance=2,
                showlegend=False,
                autosize=True,
                margin=dict(l=0, r=0, t=0, b=0),
    
                mapbox=dict(
                    accesstoken=mapbox_access_token,
                    bearing=25,
                    style='streets',
                    center=dict(
                        lat=community_center_lat, # this is the center lat-long for the selected community
                        lon=community_center_lon
                    ),
                    pitch=40,
                    zoom=12
                ),
    
            )
        
        # Creating the possible 'data' components of the map 
        
        # Existing assets points object
        existing_points = go.Scattermapbox(
            lon=map_df['longitude'],
            lat=map_df['latitude'],
            mode='markers',
            marker=dict(
                size=13, symbol=map_df['symbolBasedCategory']),
            unselected={'marker': {'opacity': 1}},
            selected={'marker': {'opacity': 0.5, 'size': 40}},
            # Displays the name of the asset when you hover over it
            hoverinfo='text',
            hovertext= map_df['asset_name'],
            # Defines the data for each point that will be drawn for other functions
            customdata=map_df.loc[:, [
                'asset_name','avg_score', 'address', 'comments']],
            )
        
        # Missing assets points object:
        missing_points = go.Scattermapbox(
            lon=missing_assets['longitude'],
            lat=missing_assets['latitude'],
            mode='markers',
            marker=dict(
                size=15),
            unselected={'marker': {'opacity': 1}},
            selected={'marker': {'opacity': 0.5, 'size': 40}},
            # Displays the name of the asset when you hover over it
            hoverinfo='text',
            hovertext= missing_assets['missing_asset_name'],
            # Defines the data for each point that will be drawn for other functions
            customdata=missing_assets.loc[:, [
                'missing_asset_name', 'description', 'address', 'justification']],
        )
        
        # Existing assets heatmap object
        existing_heat = go.Densitymapbox(
            lon=map_df['longitude'],
            lat=map_df['latitude']
            )
        
        # Missing assets heatmap object
        missing_heat = go.Densitymapbox(
            lon=missing_assets['longitude'],
            lat=missing_assets['latitude']            
            )
        
        # Heatmap of both combined
        combined = map_df[['longitude', 'latitude']].append(missing_assets[['longitude', 'latitude']])
        combined_heat = go.Densitymapbox(
            lon = combined['longitude'],
            lat = combined['latitude']
            )
    
        # Based on the options chosen, returning different 'data' components of the map
        
        if map_type == 'Points':
            
            if choose_the_source == 'All':
                locations = [existing_points, missing_points]
                
            elif choose_the_source == 'Existing Assets':
                locations = [existing_points]
            
            # Case where source = Missing assets
            else:
                locations = [missing_points]

        # Case when map type = heatmap
        elif map_type == 'Heatmap':
            
            if choose_the_source == 'All':
                locations = [combined_heat]
                
            elif choose_the_source == 'Existing Assets':
                locations = [existing_heat]
            
            # Case where source = Missing assets
            else:
                locations = [missing_heat]
        
        # Case when map type = Both
        else:
            
            if choose_the_source == 'All':
                locations = [existing_points, missing_points, combined_heat]
                
            elif choose_the_source == 'Existing Assets':
                locations = [existing_points, existing_heat]
            
            # Case where source = Missing assets
            else:
                locations = [missing_points, missing_heat]
        
        # Return the selected components to the figure
        return {
            'data': locations,
            'layout': layout
        }
