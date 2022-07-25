"""
File: submitNewAsset.py
Author: Mihir Bhaskar

Desc: This file creates the layout of the 'submit new asset' feature of the app
Input: A list with the master categories, initialised in app.py
Output: 
    - A function that returns an HTML Div containing the new asset upload popup feature
    Note that this is structured into 4 different 'modals', or 'pop-up' windows, linked
    to each other with next and back buttons. This is to split up the data entry and have 
    enough space to add sufficient explainers.

Other notes:
    - This interacts with the submitNewAsset_cb in 'application'

"""
import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

def submitNewAsset(master_categories):
    
    return html.Div([
        
        # Button that opens the 'add new asset' popup groups
        dbc.Button("Click here to submit asset", id="open-asset-submit", n_clicks=0),
        
        # First pop-up (Modal 1): basic information about the asset
        dbc.Modal([
            
            dbc.ModalHeader(dbc.ModalTitle("Know about an asset we don't have on the map? Tell us about it here!")),
            
            dbc.ModalBody([
                
                html.Div([
                    dbc.Label('Asset Name'),
                    dbc.Input(id='asset-name', required=True, type='text', placeholder='Enter Asset Name'),
                    dbc.FormText('Please be specific where possible. For example, instead of just "church", enter "Mt Rose Baptist Church"', color='secondary'),
                    ]),
                
                html.Br(),
                
                html.Div([
                    dbc.Label('Description'),
                    dbc.Input(id='asset-desc', type='text', placeholder='Enter Description'),
                    dbc.FormText('''A short description of the asset. For example, if you entered a school, is it a primary or post-secondary school?''',
                                 color='secondary'),
                    ]),
                
                html.Br(),
                
                html.Div([
                     dbc.Label('Categories (select at least one)'),
                     dcc.Dropdown(id='asset-categories',
                                     options=[{'label': i, 'value': i} for i in master_categories],
                                     value=None,
                                     multi=True),
                     dbc.FormText('''Select all the categories relating to this asset. For example, a school can come under "Education",
                                  but also "Cultural" if cultural events are held there.''', color='secondary'),
                    ]),
                
                html.Br(),
                
                html.Div([
                    dbc.Label('Website'),
                    dbc.Input(id='asset-website', type='url', placeholder='Enter website (leave blank if None)'),
                    dbc.FormText('This could also be a relevant Facebook/social media page', color='secondary'), 
                    ]),
                
                ]),
            
            dbc.ModalFooter([
                dbc.Button("Next", id='open-modal-2', n_clicks=0)
                ])
             
            ], 
            id='modal-1', 
            is_open=False, 
            size='xl'
            ),
      
        # Modal 2 - location of the asset on a map
        dbc.Modal([
            
            dbc.ModalHeader(dbc.ModalTitle("Show us where the asset is located")),
            
            dbc.ModalBody([
                html.P('''Click on the map to mark the exact location of the asset. You can keep clicking
                       on different spots to change the marker location.'''),
                  
                # This takes an output from the CB which is the geocoded address based on the current clicked lat-long on the map
                html.P(id='clicked-address'),
                
                html.Small('''Tip: You can click the + and - buttons on the side to zoom in and out, click/hold/drag the map to move it around,
                           or use the address search bar on the right to navigate to a spot'''),

                
                html.Div(id='coordinate_click_id'),
                
                html.Br(),
                        
                # Map on which users can click a point to add an asset
                dbc.Row([
                    
                    # This is just a placeholder for a callback which returns the actual map object, found in submit_new_asset_cb
                    dbc.Col(html.Div(id='submit-asset-map'), width=10),
                    
                    # Address search box + button
                    dbc.Col([
                        html.P('Search an address to zoom into on the map', style={'font-weight': 'bold'}),
                        dbc.Textarea(id='address-search', placeholder='Enter street or area', size='lg'),
                        dbc.Button('Find', id='search-address-button', n_clicks=0),
                        html.Br(),
                        html.Div(id='zoom-address-confirmation'),
                        html.Br(),
                        html.Small('''Note: you still have to click the map on the location so a marker
                                   and selected address appear'''),
                        ],
                        width=2
                        ),
                    
                    ])

                ]),
            
            dbc.ModalFooter([
                dbc.Button("Back", id='back-modal-1', n_clicks=0),
                dbc.Button("Next", id='open-modal-2_5', n_clicks=0)
                ]),
             
            ], 
            id='modal-2', 
            is_open=False, 
            size='xl'
            ),
                                   
        # Modal 2.5 (stylised modal-2_5): warning about assets already in our DB, very close to selected location
        dbc.Modal([
            
            dbc.ModalHeader(dbc.ModalTitle("Are you sure we don't already have this asset in our records?")),
            
            dbc.ModalBody([
                
                # This section shows other nearby assets to make sure the user isn't re-entering an existing asset
                html.P('''If there are assets in our records that are close to the location you selected, they will be displayed in a table below.'''),
                html.P('''If the asset you are trying to submit is shown in the table, then you can close this window. You can submit a rating, or edit the 
                       info we have about this asset by finding it on the main map page and clicking it.
                       '''),
                       
                html.P("If the asset you are trying to tell us about is not listed below, please proceed by clicking 'Next'",
                       style={"font-weight": "bold"}),
                
                html.Div(id='nearby-assets-table'),
                
                ]),
            
            dbc.ModalFooter([
                dbc.Button("Back", id='back-modal-2', n_clicks=0),
                dbc.Button("Next", id='open-modal-3', n_clicks=0)
                ]),
             
            ], 
            id='modal-2_5', 
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
                    dbc.Input(id='user-name', type='text', placeholder='Enter your name'),
                    ]),
                
                html.Br(),
                
                html.Div([
                     dbc.Label('Role in the community'),
                     dbc.Input(id='user-role', type='text', placeholder='Enter your role'),
                     dbc.FormText('''How are you involved with the community? Are you a resident? A teacher? A business owner? A town planner?''',
                                 color='secondary'),
                    ]),
                
                ]),
            
            dbc.ModalFooter([
                dbc.Button("Back", id='back-modal-2_5', n_clicks=0),
                dbc.Button("Next", id='open-modal-4', n_clicks=0),
                ])
             
            ], 
            id='modal-3', 
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
                dbc.Button('Click to submit your asset', id='submit-asset-button', n_clicks=0),
                html.Br(),
                # Container to capture the confirmation message upon submitting asset
                html.Div(id='submit-asset-confirmation'),
                
                ]),
            
            dbc.ModalFooter([
                dbc.Button("Back", id='back-modal-3', n_clicks=0)
                ])
             
            ], 
            id='modal-4', 
            is_open=False, 
            size='lg'
            ),
                   
        ])
                       
                     