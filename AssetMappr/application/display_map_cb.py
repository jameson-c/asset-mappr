from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.offline as py
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash
import numpy as np
import pandas as pd
mapbox_access_token = 'pk.eyJ1IjoicWl3YW5nYWFhIiwiYSI6ImNremtyNmxkNzR5aGwyb25mOWxocmxvOGoifQ.7ELp2wgswTdQZS_RsnW1PA'


def display_map_cb(app):
    df = pd.read_sql_table('assets_preloaded', con=db.engine)

    @app.callback(Output('graph', 'figure'),
                  [Input('recycling_type', 'value')])
    def update_figure(chosen_recycling):
        df_sub = df[(df['category'].isin(chosen_recycling))]
        # Create Figure
        locations = [go.Scattermapbox(
            lon=df_sub['LONGITUDE'],
            lat=df_sub['LATITUDE'],
            mode='markers',
            marker={'color': df_sub['color']},
            unselected={'marker': {'opacity': 1}},
            selected={'marker': {'opacity': 0.5, 'size': 25}},
            hoverinfo='text',
            hovertext=df_sub['NAME'],
            customdata=df_sub['WEBSITE']
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
                        lat=40.4406,
                        lon=-79.9959
                    ),
                    # 40.4406° N, 79.9959° W
                    pitch=40,
                    zoom=11.5
                ),
            )
        }
# ---------------------------------------------------------------
# callback for Web_link

    @app.callback(
        Output('web_link', 'children'),
        [Input('graph', 'clickData')])
    def display_click_data(clickData):
        if clickData is None:
            return 'Click on any bubble to see the website or rate it.'
        else:
            # print (clickData)
            the_link = clickData['points'][0]['customdata']
            if the_link is None:
                return 'No Website Available'
            else:
                return html.A(the_link, href=the_link, target="_blank")

# ------------------------------------------------------------------------
# callback for rating， not finished
    @app.callback(
        Output('rate', 'children'),
        [Input('graph', 'clickData')])
    def display_click_data(clickData):
        if clickData is None:
            return 'Click on any bubble to rate it.'
        else:
            # print (clickData)
            the_link = clickData['points'][0]['customdata']
            if the_link is None:
                return 'No Website Available'
            else:
                return html.A(the_link, href=the_link, target="_blank")
