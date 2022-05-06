"""
File: display_asset_info_cb
Author: Anna Wang
     
"""
import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import dcc
from dash import html
import pandas as pd

def display_asset_info_cb(app):
    
    @app.callback(
    Output('display-asset-name', 'children'),
    [Input('graph', 'clickData')])
    def display_asset_name(clickData):
        if clickData is None:
            return None
        else:
            return clickData['points'][0]['customdata'][0]
        
    @app.callback(
    Output('display-asset-desc', 'children'),
    [Input('graph', 'clickData')])
    def display_asset_desc(clickData):
        if clickData is None:
            return None
        else:
            return clickData['points'][0]['customdata'][1]
    
    @app.callback(
    Output('web_link', 'children'),
    [Input('graph', 'clickData')])
    def display_asset_website(clickData):
        if clickData is None:
            return None
        else:
            # print (clickData)
            the_link = clickData['points'][0]['customdata'][2]
            if the_link is None:
                return 'No Website Available'
            else:
                return html.A(the_link, href=the_link, target="_blank")