"""
File: title_desc.py
Author: Mihir Bhaskar

Desc: This file creates the main title and description component of the app layout
Input: 

Output: 
    A function that returns an HTML Div containing the app title and description
    
"""

import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import dcc
from dash import html

def title_desc():
   
    return html.Div(
        id="title-desc",
        children=[
            html.H5("AssetMappR"),
            html.H3("Find and contribute assets in your community"),
            html.Div(
                id="intro",
                children='''Use the search options below to find assets near you, or
                            let us know about something we may have missed.''',
                ),
            ],
        )
