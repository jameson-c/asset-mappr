"""
File: submitRating.py
Author: Anna Wang, Mihir Bhaskar

Desc: This file creates the layout of the 'submit rating' feature of the app

Input:
    - master_value_tags: the unique list of possible value tags

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
from sqlalchemy import true


def submitRating(tagList_pos):

    return html.Div([
        # How do you feel about XXX(asset-name)?
        html.Div(id='HowDoYouFeel'),

        # Slider bar to score the asset
        html.H5(
            'Use the slider below to indicate a rating, where 1 is lowest and 5 is highest:', style={'color': 'dimgray', 'font-size': '18px'}),

        # Different responses based on different rate score
        html.Div(id='rating-remind'),

        # Slider for rating
        daq.Slider(
            min=1,
            max=5,
            handleLabel={"showCurrentValue": True,
                         "label": "value"},
            step=1,
            id='rating-score',
            size=300,
        ),

        # Choose the value tags
        html.H5(
            'Why do you feel this way? Select all options that apply', style={'color': 'dimgray', 'font-size': '18px'}),

        # Value tag options
        dcc.Dropdown(
            id='value-tag',
            options=[{'label': i, 'value': i} for i in tagList_pos],
            value=None,
            multi=True
        ),

        # Text box to provide comments
        html.H5(
            'Any other specific suggestions or comments to add?', style={'color': 'dimgray', 'font-size': '18px'}),
        dcc.Textarea(
            placeholder='Share your thoughts...',
            id='rating-comments',
            value='',
        ),
        html.Br(),
        # Button to confirm submission of the rating
        html.Button(
            'Submit', id='submit-rating-button', n_clicks=0),
        html.Br(),
        html.Div(id='submit-rating-confirmation')
    ])
