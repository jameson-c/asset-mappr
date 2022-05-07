"""
File: submitRating.py
Author: Anna Wang, Mihir Bhaskar

Desc: This file creates the layout of the 'submit rating' feature of the app

Output: 
    - A function that returns an HTML Div containing the rating feature

Other notes:
    - This interacts with the submitRating_cb in 'application'

"""
import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import dcc
from dash import html
import pandas as pd

def submitRating():
    return html.Div([
                html.Label(['How do you feel about this asset?'], 
                           style={'textDecoration': 'underline', 'fontSize': 20}),
                # Slider bar to score the asset
                html.H5('Use the slider below to indicate a rating (right is better)'),
                dcc.Slider(value=2.5, min=0, max=5,
                           step=0.5, id='rating-score'),
                # Text box to provide comments
                html.H5('User the box below to share any comments or thoughts about the asset'),
                dcc.Textarea(
                    id='rating-comments',
                    value='',
                    style={'width': '100%', 'height': 30},
                ),
                # Button to confirm submission of the rating
                html.Button(
                    'Submit', id='submit-rating-button', n_clicks=0),
                html.Div(id='submit-rating-confirmation')
            ])