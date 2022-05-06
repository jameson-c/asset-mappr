from dash import dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import dash_html_components as html
import dash
import pandas as pd


def display_map_cb(app, df, asset_categories):    
    
    map_df = pd.merge(df, asset_categories, on='asset_id')        
    
    @app.callback(Output('graph', 'figure'),
                  [Input('recycling_type', 'value')])
    def update_figure(chosen_recycling):
        
        mapbox_access_token = 'pk.eyJ1IjoicWl3YW5nYWFhIiwiYSI6ImNremtyNmxkNzR5aGwyb25mOWxocmxvOGoifQ.7ELp2wgswTdQZS_RsnW1PA'
        
        df_sub = map_df[(map_df['category'].isin(chosen_recycling))]

        
        # Create figure
        locations = [go.Scattermapbox(
            lon=df_sub['longitude'],
            lat=df_sub['latitude'],
            mode='markers',
            # marker={'color': df_sub['Category']},
            unselected={'marker': {'opacity': 1}},
            selected={'marker': {'opacity': 0.5, 'size': 25}},
            hoverinfo='text',
            hovertext=df_sub['asset_name'],
            customdata=df_sub['website'],
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
                    style='light',
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