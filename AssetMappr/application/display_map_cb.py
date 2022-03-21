from dash import dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import dash_html_components as html
import dash
import pandas as pd


def display_map_cb(app, db):
    mapbox_access_token = 'pk.eyJ1IjoicWl3YW5nYWFhIiwiYSI6ImNremtyNmxkNzR5aGwyb25mOWxocmxvOGoifQ.7ELp2wgswTdQZS_RsnW1PA'
    df = pd.read_sql_table('assets', con=db.engine)
# #---------------------------------------------------------------
# # Output of Graph

    @app.callback(Output('graph', 'figure'),
                  [Input('recycling_type', 'value')])
    def update_figure(chosen_recycling):
        df_sub = df[(df['asset_type'].isin(chosen_recycling))]
        # Create figure
        locations = [go.Scattermapbox(
            lon=df_sub['latlong'], #Need to know the point data more information. should it be geometry? if so: lon=df_sub['latlong'].y
            lat=df_sub['latlong'],
            mode='markers',
            marker={'color': 'blue'},  # ***
            unselected={'marker': {'opacity': 1}},
            selected={'marker': {'opacity': 0.5, 'size': 25}},
            hoverinfo='text',
            hovertext=df_sub['asset_name'],
            customdata=df_sub['website'],
            # rating=df_sub['ratings'] need to be added into table
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
                return html.P(the_link, href=the_link, target="_blank")
