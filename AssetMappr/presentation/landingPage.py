"""
File: landingPage.py
Author: Mihir Bhaskar

Desc: This file returns an HTML Div with the content of the landing or welcome page

Output: 
    - HTML Div with the main welcome page content. This is called directly in the app.py file
"""
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

def makeLandingPage():
    
    return html.Div([
        html.H1('Welcome to AssetMappr!'),
        html.H3('(insert subtitle)'),
        html.Br(),
        
        # Link to take users to the main home page of the app
        dcc.Link('Enter the app', href='/home'),
        ])
