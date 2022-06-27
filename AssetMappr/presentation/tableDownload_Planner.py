"""
File: tableDownload_Planner.py
Author: Mihir Bhaskar

Desc: This file returns an HTML Div with the table display and download component of the planner dashboard

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
        html.Hr(),

        html.Div(className="title-what",
                children=[html.H5('What would you like to see in the table?')]),

        dbc.Row([

            dbc.Col([
                html.H6(className='subtitle-for-dropdown',
                        children=['Type of assets:'])
            ]),

        ]),
        
        dbc.Row([
            dbc.Col([
                    dcc.Dropdown(
                        id='choose-the-table-source',
                        options=[
                            {"label": "Existing Assets",
                                "value": 'Existing Assets'},
                            {"label": "Suggested 'Missing' Assets", "value": 'Missing Assets'}],
                        value='Missing Assets',
                        multi=False)
                    ], width=3),
            # Button to click to download the data in an Excel file (the data displayed in the table)
            dbc.Col([
                dbc.Button("Download data", id="download_button"),
                dcc.Download(id="download-dataframe-xlsx")
            ], width=3)

        ], className="g-0"),

        dbc.Row([
            # Place holder for the table that will be outputted by the linked callback
            html.Div(id='data-table')
        ])
    ])
