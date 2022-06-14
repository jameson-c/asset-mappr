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
from unicodedata import category
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import pandas as pd


def showMap_cb(app):
    
    # This callback receives input on which categories the user has selected (recycling_type)
    # And outputs the map object
    @app.callback(
        Output("recycling_type", "value"),
        [Input("all-or-none", "value")],
        [State("recycling_type", "options")],
    )
    def select_all_none(all_selected, options):
        all_or_none = []
        all_or_none = [option["value"] for option in options if all_selected]
        return all_or_none

    @app.callback(Output('graph', 'figure'),
                  [Input('recycling_type', 'value')],
                  
                  # Retrieves the relevant community's data from the dcc.Store object
                  [Input('assets-df', 'data')],
                  [Input('asset-categories', 'data')],
                  [Input('selected-community-info', 'data')]
                  )
    def update_figure(chosen_recycling, df, asset_categories, selected_community):
        
        # Return the JSON format data from the dcc.Store into data frames
        df = pd.read_json(df, orient='split')
        asset_categories = pd.read_json(asset_categories, orient='split')
        
        # Merge the assets and asset-category mappings into a single df
        map_df = pd.merge(df, asset_categories, on='asset_id')        

        #We should change this part when the categories are changed. Becuase each category has one symbol, it is a one on one thing, we have to manually choose the symbol for each category.
        categoryList = ["Community Centers", "Entertainment", "Financial Assistance", "Food Access",
                        "Healthcare",
                        "Housing",
                        "Libraries",
                        "Postsecondary Schools",
                        "Private Schools",
                        "Public Schools",
                        "Recreation",
                        "Religious",
                        "Service Organizations"]
        #keep it as a backup choice: You can change the color only for the circle, by now, we aren't be able to change the symbols' colors
        # colorList = ['#000000', '#003786', '#0e58a8', '#30a4ca', '#54c8df', '#9be4ef',
        #              '#e1e9d1', '#f3d573', '#e7b000', '#da8200', '#c65400',  '#498534',  '#217eb8']
        # backup color choices: '#ac2301','#001f4d','#4c0000','#217eb8',
        
        # for item in zip(categoryList, colorList):
        #     map_df.loc[map_df['category'] == item[0],
        #                'colorBasedCategory'] = item[1]
        
        
        #These symbols are from: https://labs.mapbox.com/maki-icons
        symbolList = ['town', 'amusement-park', 'bank', 'restaurant-pizza',
                      'hospital-JP',
                      'lodging',
                      'library',
                      'school',
                      'school',
                      'school',
                      'baseball',
                      'place-of-worship',
                      'town-hall']

        # Zip the categoryList and symbolList. Each category has their different symbol.
        for item in zip(categoryList, symbolList):
            map_df.loc[map_df['category'] == item[0],
                       'symbolBasedCategory'] = item[1]

        # Filtering the dataset to only keep assets in the selected categories
        df_sub = map_df[(map_df['category'].isin(chosen_recycling))]
        
        # Get the community lat-long to center on   
        selected_community = pd.read_json(selected_community, orient='split')             
        community_center_lat = float(selected_community['latitude'])
        community_center_lon = float(selected_community['longitude'])

        # Setting mapbox access token (this is for accessing their base maps)
        mapbox_access_token = 'pk.eyJ1IjoicWl3YW5nYWFhIiwiYSI6ImNremtyNmxkNzR5aGwyb25mOWxocmxvOGoifQ.7ELp2wgswTdQZS_RsnW1PA'

        # Create figure
        locations = [go.Scattermapbox(
            lon=df_sub['longitude'],
            lat=df_sub['latitude'],
            mode='markers',
            marker=dict(
                size=13, symbol=df_sub['symbolBasedCategory']),
            unselected={'marker': {'opacity': 1}},
            selected={'marker': {'opacity': 0.5, 'size': 40}},
            # Displays the name of the asset when you hover over it
            hoverinfo='text',
            hovertext=df_sub['asset_name'],
            # Defines the data for each point that will be drawn for other functions
            customdata=df_sub.loc[:, ['asset_name',
                                      'description', 'website', 'asset_id','address']],
        )]
        
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
                    zoom=11.5
                ),
            )

        # Return figure
        return {
            'data': locations,
            'layout': layout
        }
