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
    return html.Div(className='third-panel-asset-info', children=[

        html.H6(id='display-asset-name'),

        html.H6(id='display-asset-desc'),

        html.Pre(id='web_link'),

        html.H6(id='display-asset-address'),

        html.P(id='suggest-edit-instruction'),

        html.Button("Suggest an edit", id="open-edit-window",
                    n_clicks=0, hidden=True),

        # suggest an edit
        dbc.Modal([

            dbc.ModalHeader(dbc.ModalTitle(
                "Something wrong with the information about this asset? Edit the information below and click submit")),

            dbc.ModalBody([

                html.Div([
                    dbc.Label('Asset Name'),
                    dbc.Input(id='suggested-name', required=True,
                              type='text', placeholder='Enter Asset Name'),
                    dbc.FormText(
                        'Wrong name? Change it above.', color='secondary'),
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
                        '''Is there a different category that this asset should be in, other than the one
                           shown above? Change it above to tell us.''', color='secondary'),
                ]),

                html.Br(),

                html.Div([
                    dbc.Label('Description'),
                    dbc.Input(id='suggested-desc', type='text',
                              placeholder='Enter Description'),
                    dbc.FormText('''Wrong or missing description? Add or change one above.''',
                                 color='secondary'),
                ]),

                html.Br(),

                html.Div([
                    dbc.Label('Address'),
                    dbc.Input(id='suggested-address',
                              type='text', placeholder='Enter Address'),
                    dbc.FormText('''Wrong address? Enter the correct one in a clear format: street number, street, area/locality''',
                                 color='secondary'),
                ]),

                html.Br(),

                html.Div([
                    dbc.Label('Website'),
                    dbc.Input(id='suggested-website', type='url',
                              placeholder='Enter website (leave blank if None)'),
                    dbc.FormText(
                        'Wrong or missing website? Edit above. This could also be a relevant Facebook/social media page', color='secondary'),
                ]),


                html.Br(),


                html.Div([
                    dbc.Label(
                        'Is the asset closed or removed? If not, leave this blank.'),

                    dcc.Dropdown(id='current-status',
                                 options=[{'label': 'Permanently closed', 'value': 'Permanently closed'},
                                          {'label': 'Temporarily closed',
                                              'value': 'Temporarily closed'},
                                          {'label': 'Never existed',
                                              'value': 'Never existed'}
                                          ],
                                 value=None,
                                 multi=False),
                    dbc.FormText(
                        'Tell us the current status of this asset', color='secondary'),
                ]),

                dbc.Button("Submit", id='submit-suggest-button'),
                html.Div(id='submit-suggest-confirmation')

            ]),


        ],
            id='modal-sugget-edit',
            is_open=False,
            size='xl'
        ),
        html.Br()

    ])
