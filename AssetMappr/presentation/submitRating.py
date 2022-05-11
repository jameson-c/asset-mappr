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
from matplotlib import style
import dash_daq as daq


def submitRating():
    return html.Div([
        html.Label(['How do you feel about this asset?'],
                   style={'fontSize': 20}),
        html.Br(),
        # Slider bar to score the asset
        html.H5(
            'Use the slider below to indicate a rating (0-5):', style={'color': 'dimgray', 'font-size': '18px'}),
        daq.Slider(
            min=0,
            max=5,
            value=2.5,
            handleLabel={"showCurrentValue": True,
                         "label": "Rate:"},
            step=0.5,
            id='rating-score',
            size=300
        ),

        # Text box to provide comments
        html.H5(
            'Use the box below to share any comments or thoughts about the asset:', style={'color': 'dimgray', 'font-size': '18px'}),
        dcc.Textarea(
            placeholder='Share your thoughts...',
            id='rating-comments',
            value='',
            style={'width': '80%', 'height': 30},

        ),
        html.Br(),
        # Button to confirm submission of the rating
        html.Button(
            'Submit', id='submit-rating-button', n_clicks=0),
        html.Div(id='submit-rating-confirmation'
                 )
    ])
