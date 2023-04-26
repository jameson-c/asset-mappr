"""
File: surveyDownload_Planner.py
Author: Olivia Hao

Desc: This file returns an HTML Div with the table display and download component of the planner dashboard

The main table is created in surveyDownload_Planner_cb in the application folder

Input

Output:
    - HTML Div, called in makeLayout()
"""
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash import dash_table


def surveyDownload_Planner():
    return html.Div([
        html.Hr(),

        html.Div(className="title-what",
                 children=[html.H5('Which survey would you like to download?')]),

        dbc.Row([

            dbc.Col([
                html.H6(className='subtitle-for-dropdown',
                        children=['Survey Name'])
            ]),

        ]),

        dbc.Row([
            dbc.Col([
                    dcc.Dropdown(
                        id='choose-the-survey-source',
                        options=[
                            {"label": "Aquatorium Survey",
                                "value": 'Aquatorium Survey'},
                            {"label": "Placeholder Survey", "value": 'Placeholder Survey'}],
                        value='Placeholder Survey',
                        multi=False)
                    ], width=4),
            # Button to click to download the data in an Excel file (the data displayed in the table)
            dbc.Col([
                dbc.Button("Download data as CSV",
                           id="button_survey_csv"),
                dcc.Download(id="download-survey-xlsx")
            ], width=2),
            dbc.Col([
                dbc.Button("Download data as PDF",
                           id="button_survey_pdf"),
                dcc.Download(id="download-survey-pdf")
            ], width=2),

        ]),

        dbc.Row([
            # Place holder for the table that will be outputted by the linked callback
            html.Div(id='survey-table')
        ])
    ])
