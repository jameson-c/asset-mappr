"""
File: tableDownload_Planner.py
Author: Mihir Bhaskar

Desc: This file returns an HTML Div with the table download component

The main table is created in tableDownload_Planner_cb in the application folder

Input

Output:
    - HTML Div, called in makeLayout()
"""
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash import dash_table


def tableDownload_Planner():
    return html.Div([
        
        html.H5('What would you like to see in the table?'),

        dbc.Row([
            
            dbc.Col([
                html.H6('Type of assets')
                ]),
            
            dbc.Col([
                dcc.Dropdown(
                        id='choose-the-table-source',
                        options=[
                            {"label": "Existing Assets", "value": 'Existing Assets'},
                            {"label": "Suggested 'Missing' Assets", "value": 'Missing Assets'}],
                             value='Missing Assets',
                        multi=False)           
                ]),
            
            dbc.Col([
                html.Button("Download table data", id="download_button"),
                dcc.Download(id="download-dataframe-xlsx")                
                ])
        

            ]),
                
        # Place holder for the table that will be outputted by the linked callback
        html.Div(id='data-table')
                            
        ])
        
        
        