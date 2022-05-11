"""
File: showMap_cb.py
Author: Anna Wang, Mihir Bhaskar

Desc: This file creates the callback that generates the main asset map display
      
This is linked to the showMap.py feature in presentation

Input: 
    app: an initialized dash app
    df: main data frame with assets to be displayed
    asset_categories: data frame with assets and their catagories (in separate df because 1 asset can have many cats)
    
Output: 
    Callbacks relating to the showMap feature
     
"""
from dash import dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from dash import html
import dash
import pandas as pd


def showMap_cb(app, df, asset_categories):    
    
    # Merge the assets and asset-category mappings into a single df
    map_df = pd.merge(df, asset_categories, on='asset_id')        
    
    # This callback receives input on which categories the user has selected (recycling_type)
    # And outputs the map object
    @app.callback(Output('graph', 'figure'),
                  [Input('recycling_type', 'value')])
    def update_figure(chosen_recycling):
        # Nonlocal tells this nested function to access map_df from the outer function - otherwise throws an undefined error
        nonlocal map_df
        
        # Filtering the dataset to only keep assets in the selected categories
        df_sub = map_df[(map_df['category'].isin(chosen_recycling))]

        # Setting mapbox access token (this is for accessing their base maps)
        mapbox_access_token = 'pk.eyJ1IjoicWl3YW5nYWFhIiwiYSI6ImNremtyNmxkNzR5aGwyb25mOWxocmxvOGoifQ.7ELp2wgswTdQZS_RsnW1PA'

        # Create figure
        locations = [go.Scattermapbox(
            lon=df_sub['longitude'],
            lat=df_sub['latitude'],
            mode='markers',
            unselected={'marker': {'opacity': 1}},
            selected={'marker': {'opacity': 0.5, 'size': 35}},
            # Displays the name of the asset when you hover over it
            hoverinfo='text',
            hovertext=df_sub['asset_name'],
            # Defines the data for each point that will be drawn for other functions
            customdata= df_sub.loc[:,['asset_name', 'description', 'website', 'asset_id']],
        )]
    
        # Return figure
        return {
            'data': locations,
            'layout': go.Layout(
                uirevision='foo',  # preserves state of figure/map after callback activated
                clickmode='event+select',
                hovermode='closest',
                hoverdistance=2,
                showlegend=False,
                autosize=True,
                # title=dict(text="Looking for a Community Asset",font=dict(size=50, color='green')),
                margin=dict(l=0, r=0, t=0, b=0),
    
                mapbox=dict(
                    accesstoken=mapbox_access_token,
                    bearing=25,
                    style='streets',
                    center=dict(
                        lat=39.8993885,
                        lon=-79.7249338
                    ),
                    # 40.4406° N, 79.9959° W
                    pitch=40,
                    zoom=11.5
                ),
            )
        }