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
from dash import dcc
from dash import html
import dash_daq as daq


def submitRating(tagList_pos):

    return html.Div(className='third-panel-rating', children=[

        # How do you feel about XXX(asset-name)?
        html.H5(id='HowDoYouFeel'),

        # Slider bar to score the asset
        html.H5(
            'Use the slider below to indicate a rating, where 1 is lowest and 5 is highest:', style={'color': 'olivedrab', 'font-size': '14px', 'font-style': 'italic'}),

        # Different responses based on different rate score
        html.Div(id='rating-remind'),

        html.Div(id='slider', children=[
            # Slider for rating
            dcc.Slider(
                min=1,
                max=5,
                tooltip={"placement": "top", "always_visible": True},
                step=1,
                value=None,
                id='rating-score',
            ),

        ]),


        html.Br(),
        # Choose the value tags
        html.H5(
            'Why do you feel this way? Select all options that apply', style={'color': 'dimgray', 'font-size': '15px'}),

        # Value tag options
        dcc.Dropdown(
            id='value-tag',
            options=[{'label': i, 'value': i, 'title': i}
                     for i in tagList_pos],
            value=None,
            multi=True
        ),
        html.Br(),
        # Text box to provide comments
        html.H5(
            'Any other specific suggestions or comments to add?', style={'color': 'dimgray', 'font-size': '15px'}),
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
