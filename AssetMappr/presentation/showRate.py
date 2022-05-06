import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import dcc
from dash import html
import pandas as pd

def showRate():
    return html.Div([
                html.Label(['How do you feel about this asset?'], style={
                           'textDecoration': 'underline', 'fontSize': 20}),
                html.H5('Use the slider below to indicate a rating (right is better)'),
                dcc.Slider(value=2.5, min=0, max=5,
                           step=0.5, id='rating-score'),
                html.H5('User the box below to share any comments or thoughts about the asset'),
                dcc.Textarea(
                    id='rating-comments',
                    value='',
                    style={'width': '100%', 'height': 30},
                ),
                html.Button(
                    'Submit', id='submit-rating-button', n_clicks=0),
                html.Div(id='submit-rating-confirmation')
                ])