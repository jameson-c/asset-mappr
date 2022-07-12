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
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import pandas as pd
import requests
import json
import dash_html_components as html


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

    @app.callback(
        Output('graph', 'figure'),
        Output('no-result-alert', 'children'),
        [Input('recycling_type', 'value')],
        [Input('search-address-button-tab1', 'n_clicks')],
        
        # Retrieves the relevant community's data from the dcc.Store object
        [Input('assets-df', 'data')],
        [Input('selected-community-info', 'data')],
        [Input('asset-categories-cnm', 'data')],
        State('address-search-tab1', 'value'))
    
    def update_figure(chosen_recycling, n_clicks, df_cnm, selected_community, asset_categories,address_search_1):
        # Transform the JSON format data from the dcc.Store back into data frames
        df_cnm = pd.read_json(df_cnm, orient='split')
        asset_categories = pd.read_json(asset_categories, orient='split')

        selected_community = pd.read_json(selected_community, orient='split')

        # Merge the assets and asset-category mappings into a single df
        map_df = pd.merge(df_cnm, asset_categories, on='asset_id')
       
        # We should change this part when the categories are changed. Becuase each category has one symbol, it is a one on one thing, we have to manually choose the symbol for each category.
        categoryList = ["Sports and recreation", "Culture and history", "Education and workforce development",
                        "Healthcare", "Housing", "Places of worship", "Community service and assistance", "Transport and infrastructure",
                        "Food access", "Nature and parks", "Libraries", "Economic development opportunities", "Local business and economy"]
        # keep it as a backup choice: You can change the color only for the circle, by now, we aren't be able to change the symbols' colors

        # colorList = ['#000000', '#003786', '#0e58a8', '#30a4ca', '#54c8df', '#9be4ef',
        #              '#e1e9d1', '#f3d573', '#e7b000', '#da8200', '#c65400',  '#498534',  '#217eb8']
        # backup color choices: '#ac2301','#001f4d','#4c0000','#217eb8',

        # for item in zip(categoryList, colorList):
        #     map_df.loc[map_df['category'] == item[0],
        #                'colorBasedCategory'] = item[1]
        # These symbols are from: https://labs.mapbox.com/maki-icons
        symbolList = ['park', 'museum', 'school', 'hospital',
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

        # Filtering the dataset to only keep assets in the selected categories
        df_sub = map_df[(map_df['category'].isin(chosen_recycling))]
        
        # Get the community lat-long to center on (from the selected community info)
        community_center_lat = float(selected_community['latitude'])
        community_center_lon = float(selected_community['longitude'])

        # Setting mapbox access token (this is for accessing their base maps)
        mapbox_access_token = 'pk.eyJ1IjoicWl3YW5nYWFhIiwiYSI6ImNremtyNmxkNzR5aGwyb25mOWxocmxvOGoifQ.7ELp2wgswTdQZS_RsnW1PA'

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
                                      'description', 'website', 'asset_id', 'address', 'category']],
        )]

        if n_clicks == 0:
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
                    style='light',
                    center=dict(
                        lat=community_center_lat, # this is the center lat-long for the selected community
                        lon=community_center_lon
                    ),
                    pitch=40,
                    zoom=11.5
                ),
            )
            return {
                'data': locations,
                'layout': layout
            }, None

        else:
            # Geocode the lat-lng using Google Maps API
            google_api_key = 'AIzaSyDitOkTVs4g0ibg_Yt04DQqLaUYlxZ1o30'
            
            # Retrieve the name of the community to add to the geocoding search to make it more accurate
            selected_community = pd.read_json(selected_community, orient='split')
            
            community_name = selected_community['community_name'][1]

            # Adding Uniontown PA to make the search more accurate (to generalize)
            address_search = address_search_1 + community_name + ', PA'

            params = {'key': google_api_key,
                      'address': address_search}

            url = 'https://maps.googleapis.com/maps/api/geocode/json?'

            response = requests.get(url, params)
            result = json.loads(response.text)

            if result['status'] not in ['INVALID_REQUEST', 'ZERO_RESULTS']:

                lat = result['results'][0]['geometry']['location']['lat']
                lon = result['results'][0]['geometry']['location']['lng']

                layout = go.Layout(
                    uirevision=address_search_1,  # preserves state of figure/map after callback activated
                    clickmode='event+select',
                    hovermode='closest',
                    hoverdistance=2,
                    showlegend=False,
                    autosize=True,
                    margin=dict(l=0, r=0, t=0, b=0),

                    mapbox=dict(
                        accesstoken=mapbox_access_token,
                        bearing=25,
                        style='light',
                        center=dict(
                            lat=lat,
                            lon=lon
                        ),
                        pitch=40,
                        zoom=16
                    )
                )

                # Return figure
                return {
                    'data': locations,
                    'layout': layout
                }, None
            else:
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
                        style='light',
                        center=dict(
                            lat=community_center_lat, # this is the center lat-long for the selected community
                            lon=community_center_lon
                        ),
                        pitch=40,
                        zoom=11.5
                    ),
                )
                return {
                    'data': locations,
                    'layout': layout
                }, html.Div("invalid address")
