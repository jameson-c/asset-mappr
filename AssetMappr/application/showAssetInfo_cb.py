"""
File: showAssetInfo_cb
Author: Anna Wang, Mihir Bhaskar

Desc: This file creates the callbacks that display information about the selected asset
on the map.
      
This is linked to the showAssetInfo.py layout file, as well as the showMap_cb because 
the callbacks take inputs from the map click events (when a user clicks on an asset)

Input: 
    app: an initialized dash app
    
Output: 
    Callbacks relating to the showAssetInfo feature
     
"""
import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import dcc
from dash import html

import pandas as pd

import dash_bootstrap_components as dbc


def showAssetInfo_cb(app):

    # Callback to fetch the asset name from the point clicked on the map
    # Note: this and all callbacks below rely on clickData that is defined in the
    # showMap_cb file. The map/graph contains customdata about each point
    @app.callback(
        Output('display-asset-name', 'children'),
        [Input('graph', 'clickData')])
    def display_asset_name(clickData):
        if clickData is None:
            return None
        else:
            # clickData is a JSON style dictionary, with the customdata field
            # containing a data frame with relevant information about the clicked point
            asset_name = clickData['points'][0]['customdata'][0]
            return 'Name: {}'.format(asset_name)

    # Callback to fetch the asset description
    @app.callback(
        Output('display-asset-desc', 'children'),
        [Input('graph', 'clickData')])
    def display_asset_desc(clickData):
        if clickData is None:
            return None
        else:
            description = clickData['points'][0]['customdata'][1]
            return 'Description: {}'.format(description)

    # Callback to fetch the website
    @app.callback(
        Output('web_link', 'children'),
        [Input('graph', 'clickData')])
    def display_asset_website(clickData):
        if clickData is None:
            return None
        else:
            the_link = clickData['points'][0]['customdata'][2]
            if the_link is None:
                return 'No Website Available'
            else:
                # Returns the website as a clickable link
                return 'Website:', html.A(the_link, href=the_link, target="_blank")

    # Show the address. And clicking it will lead to google map direction page.
    @app.callback(
        Output('display-asset-address', 'children'),
        [Input('graph', 'clickData')])
    def display_asset_desc(clickData):
        if clickData is None:
            return None
        else:
            addressLink = clickData['points'][0]['customdata'][4]
            return 'Address','\n',html.A(addressLink, href='https://www.google.com/maps/dir/?api=1&AIzaSyDitOkTVs4g0ibg_Yt04DQqLaUYlxZ1o30&destination={}+PA'.format(addressLink), target="_blank")

    # Show the instruction/option to open the 'suggest an edit' feature
    @app.callback(
        Output('suggest-edit-instruction', 'children'),
        [Input('graph', 'clickData')]
        )
    def show_suggest_edit_instruction(clickData):
        if clickData is None:
            return None
        else:
            return '''Is this information, or the asset itself, wrong? 
                      Click below to suggest an edit to our records:'''

    @app.callback(Output('open-edit-window', 'hidden'),
                  [Input('graph', 'clickData')])
    def show_suggest_edit_button(clickData):
        if clickData is None:
            return True
        else:
            return False

    @app.callback(
        Output('modal-sugget-edit', 'is_open'),
        [Input('open-edit-window', 'n_clicks')],
        [State('modal-sugget-edit', 'is_open')]
    )
    def toggle_modal(n0, is_open):
        if n0:
            return not is_open
        return is_open
    