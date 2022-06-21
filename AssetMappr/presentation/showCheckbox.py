"""
File: showCheckbox.py
Author: Anna Wang

Desc: This file returns an HTML Div with the category selection

The main map is created in showMap_cb in the application folder

Input: master_categories: a list of the unique categories of assets

Output:
    - HTML Div, called in makeLayout()
"""
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc


def showCheckbox(master_categories):
    return html.Div(className='first-panel', children=[
        # search bar
        dbc.Row([
            dbc.Textarea(id='address-search-tab1',
                         placeholder='Search for the street or area'),
            dbc.Button('Find', id='search-address-button-tab1', n_clicks=0),
            html.Div(id='no-result-alert')]),
        html.Br(),
        # Checklist to select categories of assets to display on the map
        dcc.Checklist(
            id="all-or-none",
            options=[{"label": "Select All", "value": "All"}],
            value=["All"],
            labelStyle={"display": "inline-block"},
        ),
        # Checklist with options drawing from master_categories list
        dcc.Checklist(id="recycling_type",
                      value=[x for x in master_categories],
                      options=[
                          {'label': str(x), 'value': x} for x in master_categories]),
        html.Hr()
    ])
