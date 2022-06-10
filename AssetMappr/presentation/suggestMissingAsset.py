"""
File: suggestMissingAsset.py
Author: Mihir Bhaskar

Desc: This file creates the layout of the 'suggest_missing_asset' feature of the app
Input: A list with the master categories, initialised in app.py
Output: 
    - A function that returns an HTML Div containing the suggest missing asset upload popup feature

Other notes:
    - This interacts with the suggestMissingAsset_cb in 'application'

"""
import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash_leaflet as dl

def suggestMissingAsset(master_categories):
    
    return html.Div([
        
        html.H4('Is there something missing in your community, that you would like to see?', id='missing-asset-intro'),
        html.H5('Click the button below \U0001f447 to tell us about your idea', id='click-missing-asset-button'),
        
        html.Br(),
        
        # Button that opens the 'add new asset' popup groups
        dbc.Button("Click to submit suggestion", id="open-suggest-missing-submit", n_clicks=0),
        
        # First pop-up (Modal 1): basic information about the asset
        dbc.Modal([
            
            dbc.ModalHeader(dbc.ModalTitle("Basic details")),

            dbc.ModalBody([
                
                html.Div([
                    dbc.Label("Name of the 'missing' asset"),
                    dbc.Input(id='missing-asset-name', required=True, type='text', 
                                      placeholder='Enter name'),
                    dbc.FormText("For example: 'restaurant', 'fresh grocery store', 'park', etc.",
                                 color='secondary'),                   
                    ]),
                
                html.Br(),
                
                html.Div([
                    dbc.Label('Short description'),
                    dbc.Textarea(id='missing-asset-desc', placeholder='Enter description'),
                    dbc.FormText("Additional details about your suggested asset",
                                 color='secondary'),                 
                    ]),
                
                html.Br(),
                
                html.Div([
                    dbc.Label('Main category' ),
                    dcc.Dropdown(id='missing-asset-categories',
                                    options=[{'label': i, 'value': i} for i in master_categories],
                                    value=None, 
                                    multi=False),
                    dbc.FormText('Select the main category your suggested asset belongs to',
                                 color='secondary'),                 
                    ]),
                
                html.Br(),
                
                html.Div([
                    dbc.Label('Why do you think this asset would be good for the community?'),
                    dbc.Input(id='missing-asset-justification', type='text', required=True, placeholder='Enter text'),
                    dbc.FormText('''Tell us why you think this asset is important''', color='secondary'), 
                    ]),
                
                ]),
            
            dbc.ModalFooter([
                dbc.Button("Next", id='open-modal-2-missing', n_clicks=0)
                ])
             
            ], 
            id='modal-1-missing', 
            is_open=False, 
            size='xl'
            ),


        # Modal 2 - location of the asset on a map
        dbc.Modal([
            
            dbc.ModalHeader(dbc.ModalTitle("Show us where the asset should be located")),
            
            dbc.ModalBody([
                html.P('''If there is an area or location you had in mind, click on the map to mark the where you think this asset should be
                          It can be approximate.'''),
                html.P('''You can keep clicking
                       on different spots to change the marker location.'''),
                       
                html.P(id='clicked-address-missing-asset'),
                       
                html.Small('Tip: You can click the + and - buttons on the side to zoom in and out, and click/hold/drag the map to move it around.'),

                html.Div(id='missing_coordinate_click_id'),
                        
                # Map on which users can click a point to add an asset
                # This is just a placeholder for a callback which returns the actual map object, found in submit_new_asset_cb
                html.Div(id='submit-missing-asset-map'),                

                ]),
            
            dbc.ModalFooter([
                dbc.Button("Back", id='back-modal-1-missing', n_clicks=0),
                dbc.Button("Next", id='open-modal-3-missing', n_clicks=0)
                ]),
             
            ], 
            id='modal-2-missing', 
            is_open=False, 
            size='xl'
            ),
                    
        
        # Modal 3: information about the user
        dbc.Modal([
            
            dbc.ModalHeader(dbc.ModalTitle("A bit about yourself")),
            
            dbc.ModalBody([
                
                html.P('''We'd love to know a little bit about you to help us understand who is using the site.
                        We do not share this information with anyone, and only use it to improve the site.'''),
                        
                html.B('Please feel free to skip this section and click next if you are not comfortable sharing this information.'),
                
                html.Br(),
                
                html.Div([
                    dbc.Label('Your name'),
                    dbc.Input(id='missing-user-name', type='text', placeholder='Enter your name'),
                    ]),
                
                html.Br(),
                
                html.Div([
                     dbc.Label('Role in the community'),
                     dbc.Input(id='missing-user-role', type='text', placeholder='Enter your role'),
                     dbc.FormText('''How are you involved with the community? Are you a resident? A teacher? A business owner? A town planner?''',
                                 color='secondary'),
                    ]),
                
                ]),
            
            dbc.ModalFooter([
                dbc.Button("Back", id='back-modal-2-missing', n_clicks=0),
                dbc.Button("Next", id='open-modal-4-missing', n_clicks=0),
                ])
             
            ], 
            id='modal-3-missing', 
            is_open=False, 
            size='lg'
            ),
                  
        # Modal 4: final submit button, to submit all the info
        dbc.Modal([
            
            dbc.ModalHeader(dbc.ModalTitle("Final submission")),
            
            dbc.ModalBody([
                
                html.P('''Click the button below to submit the information entered in the previous screens. If you'd like to change anything,
                       press the back buttons and edit before clicking submit.'''),
                        
                html.Br(),
                # This is the button for users to click to confirm they are submitting the asset
                dbc.Button('Click to submit your suggestion', id='submit-suggestion-button', n_clicks=0),
                html.Br(),
                # Container to capture the confirmation message upon submitting asset
                html.Div(id='submit-suggestion-confirmation'),
                
                ]),
            
            dbc.ModalFooter([
                dbc.Button("Back", id='back-modal-3-missing', n_clicks=0)
                ])
             
            ], 
            id='modal-4-missing', 
            is_open=False, 
            size='lg'
            ),
                   
        ])
                       