"""
File: submit_new_asset.py
Author: Mihir Bhaskar

Desc: This file creates the layout of the 'submit new asset' feature of the app
Input: A list with the master categories, initialised in app.py
Output: 
    - A function that returns an HTML Div containing the new asset upload popup feature

Other notes:
    - This interacts with the submit_new_asset_cb in 'application'

"""
import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash_leaflet as dl

def submit_new_asset(master_categories):
    
    return html.Div([
        
        # Button that opens the add asset popup
        dbc.Button("Click here to submit asset", id="open-asset-submit", n_clicks=0),
        
        # Pop-up object (called a 'Modal')
        dbc.Modal([
            
            dbc.ModalHeader(dbc.ModalTitle("Know about an asset we don't have? Tell us about it here!")),
            
            dbc.ModalBody([
                # Using a grid layout to split input boxes between rows and columns
                dbc.Row([
                    dbc.Col([
                        dbc.Label('Asset Name'),
                        dbc.Input(id='asset-name', required=True, type='text', placeholder='Enter Asset Name'),
                        ]),
                    dbc.Col([
                        dbc.Label('Name of user (optional)'),
                        dbc.Input(id='user-name', type='text', placeholder='Enter your name'),
                        ]),
                    ]),
                dbc.Row([
                    dbc.Col([
                         dbc.Label('Categories (select at least one)'),
                         dcc.Dropdown(id='asset-categories',
                                          options=[{'label': i, 'value': i} for i in master_categories],
                                          value=None,
                                          multi=True),
                        ]),
                    dbc.Col([
                        dbc.Label('Role in the community'),
                        dbc.Input(id='user-role', type='text', placeholder='Enter your role (e.g. resident, teacher, business owner)'),
                        ]),
                    ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label('A short description'),
                        dbc.Input(id='asset-desc', type='text', placeholder='Description of the asset'),
                        ]),
                    dbc.Col([
                        dbc.Label('Website'),
                        dbc.Input(id='asset-website', type='url', placeholder='Relevant website for the asset'),
                        ]),
                    ]),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        html.H6('Click on the map to mark the exact location of the asset'),
                        html.Div(id='coordinate_click_id'),
                        
                        # Map on which users can click a point to add an asse
                        html.Div(id='submit-asset-map'),
                        
                        ], width=10), 
                    dbc.Col([
                        html.Br(),
                        dbc.Button('Click here to submit your asset', id='submit-asset-button', n_clicks=0),
                        html.Br(),
                        # Container to capture the confirmation message upon submitting asset
                        html.Div(id='submit-asset-confirmation'),
                        ])
                    ])
                ]),
            dbc.ModalFooter(
                dbc.Button("Close", id='close-asset-submit', n_clicks=0)
                )
            ],
            id='submit-asset-modal',
            is_open=False,
            fullscreen=True,
            )
        ])