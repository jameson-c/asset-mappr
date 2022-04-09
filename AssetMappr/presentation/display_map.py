
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dash.dependencies import Input, Output, State
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

app = dash.Dash(__name__)
server = app.server

# Connect to the Heroku postgreSQL database
server.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ilohghqbmiloiv:f4fbd28e91d021bada72701576d41107b78bc515ad0b1e94d934939fbce7b2e6@ec2-54-235-98-1.compute-1.amazonaws.com:5432/dmt6i1v8bv5l1'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)
df = pd.read_sql_table('assets', con=db.engine)
# set colors:
# dic_color = {"Community Centers":'red',
#              "Cultural":'blue',
#              "Financial Assistance":'green',
#              "Food Access":'yellow',
#              "Housing":'purple',
#              "Libraries" :'orange',
#             "Recreation" : 'moccasin',
#             "Service Organization" : 'pink',
#             "Workforce Development" : 'olivedrab'
#              }
cat = ["Community Centers", "Cultural", "Financial Assistance", "Food Access",
       "Housing", "Libraries", "Recreation", "Service Organization", "Workforce Development"]
col = ['red', 'blue', 'green', 'yellow', 'purple',
       'orange', 'moccasin', 'pink', 'olivedrab']
# df.loc[df['category'] == 'Community Centers', 'color'] = 'red'
# df.loc[df['category'] == 'Cultural', 'color'] = 'blue'
# df.loc[df['category'] == 'Financial Assistance', 'color'] = 'green'
# df.loc[df['category'] == 'Food Access', 'color'] = 'yellow'
# df.loc[df['category'] == 'Housing', 'color'] = 'purple'
# df.loc[df['category'] == 'Libraries', 'color'] = 'orange'
# df.loc[df['category'] == 'Recreation', 'color'] = 'moccasin'
# df.loc[df['category'] == 'Service Organization', 'color'] = 'pink'
# # df.loc[df['category'] == 'Workforce Development', 'color'] = 'olivedrab'

# df.loc[df['category'] == 'Community Centers', 'color'] = '#FF0000'
# df.loc[df['category'] == 'Cultural', 'color'] = '#00FFFF'
# df.loc[df['category'] == 'Financial Assistance', 'color'] = '#0000FF'
# df.loc[df['category'] == 'Food Access', 'color'] = '#00008B'
# df.loc[df['category'] == 'Housing', 'color'] = '#ADD8E6'
# df.loc[df['category'] == 'Libraries', 'color'] = '#800080'
# df.loc[df['category'] == 'Recreation', 'color'] = '#FFFF00'
# df.loc[df['category'] == 'Service Organization', 'color'] = '#00FF00'
# df.loc[df['category'] == 'Workforce Development', 'color'] = '#FF00FF'


def display_map(app):
    mapbox_access_token = 'pk.eyJ1IjoicWl3YW5nYWFhIiwiYSI6ImNremtyNmxkNzR5aGwyb25mOWxocmxvOGoifQ.7ELp2wgswTdQZS_RsnW1PA'
    df = pd.read_sql_table('assets', con=db.engine)
# #---------------------------------------------------------------
# # Output of Graph

    @app.callback(Output('graph', 'figure'),
                  [Input('recycling_type', 'value')])
    def update_figure(chosen_recycling):
        df_sub = df[(df['category'].isin(chosen_recycling))]
        # Create figure
        locations = [go.Scattermapbox(
            lon=df_sub['longitude'],
            lat=df_sub['latitude'],
            mode='markers',
            # marker=dict(
            #     size=14,
            # ),
            # # marker=dict(size=14,
            # #             color=[]),
            marker={'color': 'red'},
            unselected={'marker': {'opacity': 1}},
            selected={'marker': {'opacity': 0.5, 'size': 25}},
            hoverinfo='text',
            hovertext=df_sub['name'],
            customdata=df_sub['website']
        )]

        # Return figure
        return {
            'data': locations,
            'layout': go.Layout(
                uirevision='foo',  # preserves state of figure/map after callback activated
                clickmode='event+select',
                hovermode='closest',
                hoverdistance=2,
                showlegend=True,
                autosize=True,
                # title=dict(text="Looking for a Community Asset",font=dict(size=50, color='green')),
                margin=dict(l=0, r=0, t=0, b=0),

                mapbox=dict(
                    accesstoken=mapbox_access_token,
                    bearing=0,
                    style='light',
                    # center=dict(
                    #     lat=40.4406,
                    #     lon=-79.9959
                    # ),
                    center=go.layout.mapbox.Center(
                        lat=39.90,
                        lon=-79.70
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
    # callback for rating

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
