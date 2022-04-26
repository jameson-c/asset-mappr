"""
File: submit_new_asset.py
Author: Mihir Bhaskar

Desc: This file creates the 'submitting new asset info' component of the app
Input: 
   

Output: 
    - A function that returns an HTML Div containing the user new asset upload popup feature
    
"""
import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

import dash_leaflet as dl



def submit_new_asset(master_categories):
    
    # # Old code fo creating map using Mapbox
    # fig = go.Figure()
    # fig.add_trace(go.Scattermapbox())
    
    # fig.update_layout(clickmode='event+select',
    #     mapbox=dict(accesstoken='pk.eyJ1IjoicWl3YW5nYWFhIiwiYSI6ImNremtyNmxkNzR5aGwyb25mOWxocmxvOGoifQ.7ELp2wgswTdQZS_RsnW1PA',
    #     style='mapbox://styles/mapbox/streets-v11',
    #     zoom=12.5,
    #     center= dict(
    #                     lat=39.8993885,
    #                     lon=-79.7249338
    #                 )))
    
    
    
    return html.Div([
        
        # Button that opens the add asset popup
        dbc.Button("Click here to submit asset", id="open-asset-submit", n_clicks=0),
        
        # Pop-up object
        dbc.Modal([
            
            dbc.ModalHeader(dbc.ModalTitle("Know about an asset we don't have? Tell us about it here!")),
            
            dbc.ModalBody([
                
                dbc.Form([
                    
                        dbc.Label('Name of user (optional)'),
                        dbc.Input(id='user-name', type='text', placeholder='Enter User Name'),
                        
                        dbc.Label('Role in the community (e.g. resident, teacher, business owner)'),
                        dbc.Input(id='user-role', type='text', placeholder='Enter User Role'),
                        
                        dbc.Label('Asset Name'),
                        dbc.Input(id='asset-name', required=True, type='text', placeholder='Enter Asset Name'),
                        
                    
                        dbc.Label('Categories'),
                        dcc.Dropdown(id='asset-categories',
                                      options=[{'label': i, 'value': i} for i in master_categories],
                                      value=None,
                                      multi=True),
                       
                        dbc.Label('A short description'),
                        dbc.Input(id='asset-desc', type='text', placeholder='Description'),
                        
                    
                        dbc.Label('Website'),
                        dbc.Input(id='asset-website', type='url', placeholder='Website'),
                    
                    ]),
                
                html.Br(),
                html.H6('Click on the map to mark the exact location of the asset'),
                html.Div(id='coordinate_click_id'),
                
                # Map on which users can click a point to add an asse
                html.Div(id='submit-asset-map'),
                
                dbc.Button('Click here to submit your asset', id='submit-asset-button', n_clicks=0),
                    
                html.Div(id='submit-asset-confirmation'),
                
    
                
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