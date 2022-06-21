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
    
    # Merge the assets and asset-category mappings into a single df
    map_df = pd.merge(df, asset_categories, on='asset_id')
    avg_rating = rating_score.groupby(
        'asset_id').agg({'rating_scale': [np.mean]})
    pd.set_option('display.max_columns', None)
    map_df = pd.merge(map_df, avg_rating,on='asset_id', how='left')
    map_df['avg_score'] = map_df.iloc[:,-1]
    map_df = pd.merge(map_df,rating_score,on='asset_id',how='left')
    
    # This callback receives input on which categories the user has selected (recycling_type)
    # And outputs the map object
    @app.callback(Output('graph-for-planner', 'figure'),
                  [Input('choose-the-source', 'value')],
                  [Input('map-type', 'value')])
    def update_figure(choose_the_source, map_type):
        # Nonlocal tells this nested function to access map_df from the outer function - otherwise throws an undefined error
        nonlocal map_df
        # We should change this part when the categories are changed. Becuase each category has one symbol, it is a one on one thing, we have to manually choose the symbol for each category.
        categoryList = ["Sports and recreation", "Culture and history", "Education and workforce development",
                        "Healthcare", "Housing", "Places of worship", "Community service and assistance", "Transport and infrastructure",
                        "Food access", "Nature and parks", "Libraries", "Economic development opportunities", "Local business and economy"]
        #keep it as a backup choice: You can change the color only for the circle, by now, we aren't be able to change the symbols' colors

        # colorList = ['#000000', '#003786', '#0e58a8', '#30a4ca', '#54c8df', '#9be4ef',
        #              '#e1e9d1', '#f3d573', '#e7b000', '#da8200', '#c65400',  '#498534',  '#217eb8']
        # backup color choices: '#ac2301','#001f4d','#4c0000','#217eb8',

        # for item in zip(categoryList, colorList):
        #     map_df.loc[map_df['category'] == item[0],
        #                'colorBasedCategory'] = item[1]
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
                        lat=39.8993885,
                        lon=-79.7249338
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
