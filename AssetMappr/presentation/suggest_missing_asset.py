"""
File: suggest_missing_asset.py
Author: Mihir Bhaskar

Desc: This file creates the layout of the 'suggest_missing_asset' feature of the app
Input: A list with the master categories, initialised in app.py
Output: 
    - A function that returns an HTML Div containing the suggest missing asset upload popup feature

Other notes:
    - This interacts with the suggest_new_asset_cb in 'application'

"""

import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash_leaflet as dl

def suggest_missing_asset(master_categories):
    
    return html.Div([
        
        # Button that opens the 'suggest missing asset' popup
        dbc.Button("Click here to suggest missing asset", id="open-suggest-missing-submit", n_clicks=0),
        
        # Pop-up object (called a 'Modal')
        dbc.Modal([
            
            dbc.ModalHeader(dbc.ModalTitle("Suggest 'missing' assets the community should prioritize")),
            
            dbc.ModalBody([
                # Using a grid layout to split input boxes between rows and columns
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label('Missing asset name'),
                        dbc.Input(id='missing-asset-name', required=True, type='text', placeholder='Enter name of missing asset'),
                        ]),
                    dbc.Col([
                        dbc.Label('Name of user (optional)'),
                        dbc.Input(id='missing-user-name', type='text', placeholder='Enter your name'),
                        ]),
                    ]),
                
                # Row 2
                dbc.Row([
                    # Single-select dropdown for asset categories, with the category values populated from
                    # the master_categories list that is loaded on app initialisation from readDB()
                    dbc.Col([
                         dbc.Label('Categories (select the main category)'),
                         dcc.Dropdown(id='missing-asset-categories',
                                          options=[{'label': i, 'value': i} for i in master_categories],
                                          value=None,
                                          multi=False),
                        ]),
                    dbc.Col([
                        dbc.Label('Role in the community'),
                        dbc.Input(id='missing-user-role', type='text', placeholder='Enter your role (e.g. resident, teacher, business owner)'),
                        ]),
                    ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label('A short description'),
                        dbc.Input(id='missing-asset-desc', type='text', placeholder='Description of the missing asset'),
                        ]),
                    ]),
                # html.Br() adds a line break for some blank space
                html.Br(), 
                dbc.Row([
                    dbc.Col([
                        # Instruction for the user
                        html.H6('Where should the asset be located?'),
                        html.Div(id='missing_coordinate_click_id'),
                        
                        # Map on which users can click a point to add an asset
                        # This is just a placeholder for a callback which returns the actual map object, found in suggest_missing_asset_cb
                        html.Div(id='missing-asset-map'),
                        
                        ], width=10), 
                    
                    dbc.Col([
                        html.Br(),
                        # This is the button for users to click to confirm they are suggesting the missing asset
                        dbc.Button('Click here to submit your suggestion', id='submit-suggestion-button', n_clicks=0),
                        html.Br(),
                        # Container to capture the confirmation message upon submitting asset
                        html.Div(id='submit-suggestion-confirmation'),
                        ])
                    ])
                ]),
            # The button below, which is the footer of the modal, closes the pop-up window
            dbc.ModalFooter(
                dbc.Button("Close", id="close-suggest-missing-submit", n_clicks=0)
                )
            ],
            id='suggest-missing-asset-modal',
            is_open=False, # The pop-up isn't open by default
            fullscreen=True, # The pop-up takes up the full screen 
            )
        ])