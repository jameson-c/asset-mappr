"""
File: submitNewAsset.py
Author: Mihir Bhaskar

Desc: This file creates the layout of the 'submit new asset' feature of the app
Input: A list with the master categories, initialised in app.py
Output: 
    - A function that returns an HTML Div containing the new asset upload popup feature

Other notes:
    - This interacts with the submitNewAsset_cb in 'application'

"""
import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash_leaflet as dl

def submitNewAsset(master_categories):
    
    return html.Div([
        
        # Button that opens the 'add new asset' popup
        dbc.Button("Click here to submit asset", id="open-asset-submit", n_clicks=0),
        
        # First section of the Modal
        dbc.Modal([
            
            dbc.ModalHeader(dbc.ModalTitle("Know about an asset we don't have on the map? Tell us about it here!")),
            
            dbc.ModalBody([
                
                html.Div([
                    dbc.Label('Asset Name'),
                    dbc.Input(id='asset-name', required=True, type='text', placeholder='Enter Asset Name'),
                    dbc.FormText('Please be specific: e.g. "Mt Rose Baptist Church", instead of "Church"', color='secondary'),
                    ]),
                
                html.Div([
                    dbc.Label('Description'),
                    dbc.Input(id='asset-desc', type='text', placeholder='Enter Description'),
                    dbc.FormText('''A short description of the asset. E.g. If you entered a school, is it a primary or post-secondary school?''',
                                 color='secondary'),
                    ]),
                
                html.Div([
                     dbc.Label('Categories (select at least one)'),
                     dcc.Dropdown(id='asset-categories',
                                     options=[{'label': i, 'value': i} for i in master_categories],
                                     value=None,
                                     multi=True),
                     dbc.FormText('''Select all the categories relating to this asset. E.g. a school can come under "Education",
                                  but also "Cultural" if cultural events are held there.''', color='secondary'),
                    ]),
                         
                html.Div([
                    dbc.Label('Website (optional)'),
                    dbc.Input(id='asset-website', type='url', placeholder='Enter website (leave blank if None)'),
                    dbc.FormText('This could also be a relevant Facebook/social media page'), 
                    ]),
                
                ]),
            
            dbc.ModalFooter([
                dbc.Button("Next", id='open-modal-2', n_clicks=0)
                ])
             
            ], 
            id='modal-1', 
            is_open=False, 
            size='lg'
            ),
      
        # Second section of the Modal
        dbc.Modal([
            
            dbc.ModalHeader(dbc.ModalTitle("Show us where the asset is located")),
            
            dbc.ModalBody([
                html.P('''Click on the map to mark the exact location of the asset. You can keep clicking
                       on different spots to change the marker.'''),

                html.Div(id='coordinate_click_id'),
                        
                # Map on which users can click a point to add an asset
                # This is just a placeholder for a callback which returns the actual map object, found in submit_new_asset_cb
                html.Div(id='submit-asset-map'),                

                ]),
            
            dbc.ModalFooter([
                dbc.Button("Back", id='back-modal-1', n_clicks=0),
                dbc.Button("Next", id='open-modal-3', n_clicks=0)
                ]),
             
            ], 
            id='modal-2', 
            is_open=False, 
            size='lg'
            ),

        # Third section of the Modal
        dbc.Modal([
            
            dbc.ModalHeader(dbc.ModalTitle("Submit the asset")),
            
            dbc.ModalBody([
                
                html.H6(''),
                
                html.Div([
                    dbc.Label('Name of user (optional)'),
                    dbc.Input(id='user-name', type='text', placeholder='Enter your name'),
                    dbc.FormText('''A short description of the asset. E.g. If you entered a school, is it a primary or post-secondary school?''',
                                 color='secondary'),
                    ]),
                
                html.Div([
                     dbc.Label('Role in the community'),
                     dbc.Input(id='user-role', type='text', placeholder='Enter your role (e.g. resident, teacher, business owner)'),
                     dbc.FormText('''A short description of the asset. E.g. If you entered a school, is it a primary or post-secondary school?''',
                                 color='secondary'),
                    ]),
                
                html.Hr(),
               
                html.Br(),
                # This is the button for users to click to confirm they are submitting the asset
                dbc.Button('Click here to submit your asset', id='submit-asset-button', n_clicks=0),
                html.Br(),
                # Container to capture the confirmation message upon submitting asset
                html.Div(id='submit-asset-confirmation'),
                
                ]),
            
            dbc.ModalFooter([
                dbc.Button("Back", id='back-modal-2', n_clicks=0),
                ])
             
            ], 
            id='modal-3', 
            is_open=False, 
            size='lg'
            ),
                   
        ])