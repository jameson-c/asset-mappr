"""
File: showAssetInfo.py
Author: Mihir Bhaskar, Anna Wang

Desc: This file returns an HTML Div with information about the selected asset on the asset map

These elements take inputs from showAssetInfo_cb in the application folder

Output: 
    - HTML Div, called in makeLayout()
"""

from dash import html
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from dash import dcc


def showAssetInfo(master_categories):
    return html.Div([
        html.H6(id='display-asset-name'),

        html.H6(id='display-asset-desc'),

        html.Pre(id='web_link'),

        html.H6(id='display-asset-address'),

        html.Button("Sugget an edit", id="open-edit-window",
                    n_clicks=0, hidden=True),
        
        #suggest an edit
        dbc.Modal([

            dbc.ModalHeader(dbc.ModalTitle(
                "Something wrong with these information? Tell us about it here!")),

            dbc.ModalBody([

                html.Div([
                    dbc.Label('Asset Name'),
                    dbc.Input(id='suggested-name', required=True,
                              type='text', placeholder='Enter Asset Name'),
                    dbc.FormText(
                        'Wrong name?', color='secondary'),
                ]),

                html.Br(),

                html.Div([
                    dbc.Label('Description'),
                    dbc.Input(id='suggested-desc', type='text',
                              placeholder='Enter Description'),
                    dbc.FormText('''A short description of the asset. For example, if you entered a school, is it a primary or post-secondary school?''',
                                 color='secondary'),
                ]),

                html.Br(),

                html.Div([
                    dbc.Label('Address'),
                    dbc.Input(id='suggested-address',
                              type='text', placeholder='Enter Address'),
                    dbc.FormText('''Address''',
                                 color='secondary'),
                ]),

                html.Br(),

                html.Div([
                    dbc.Label('Website'),
                    dbc.Input(id='suggested-website', type='url',
                              placeholder='Enter website (leave blank if None)'),
                    dbc.FormText(
                        'This could also be a relevant Facebook/social media page', color='secondary'),
                ]),

                html.Br(),

                html.Div([
                    dbc.Label('Close or Remove'),
                    dbc.Input(
                        id='current-status', placeholder='temporarily closed, permanently closed, does not exist here'),
                    dbc.FormText(
                        'Tell us the current status of this asset', color='secondary'),
                ]),

                html.Br(),

                html.Div([
                    dbc.Label('Category'),
                    dcc.Dropdown(id='suggested-categories',
                                 options=[{'label': i, 'value': i}
                                          for i in master_categories],
                                 value=None,
                                 multi=False),
                    dbc.FormText(
                        '''Select the category relating to this asset.''', color='secondary'),
                ]),

                dbc.Button("Submit", id='submit-suggest-button'),
                html.Div(id='submit-suggest-confirmation')

            ]),


        ],
            id='modal-sugget-edit',
            is_open=False,
            size='xl'
        )

    ])
