"""
File: submit_new_asset.py
Author: Mihir Bhaskar

Desc: This file creates the 'submitting new asset info' component of the app
Input: 
   

Output: 
    - A function that returns an HTML Div containing the user new asset upload features
    
"""
import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import dcc
from dash import html

def submit_new_asset():
    
    return html.Div(
        id="submit-new-asset",
        children=[
            # Entering name
            html.P("Enter the asset's name"),
            dcc.Input(id='asset-name', value='', type='text')
        ]
    )