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
import dash_leaflet as dl


def submit_new_asset():
    
    return html.Div([
        
        # Button that opens the add asset popup
        dbc.Button("Click here to submit asset", id="open-asset-submit", n_clicks=0),
        
        # Pop-up object
        dbc.Modal([
            
            dbc.ModalHeader(dbc.ModalTitle('Add an asset')),
            
            dbc.ModalBody([
                
                
                dbc.Form([
                    
                    dbc.FormGroup([
                        dbc.Label('Asset Name'),
                        dbc.Input(id='asset-name', type='text', placeholder='Enter Asset Name'),
                        ]),
                    
                    dbc.FormGroup([
                        dbc.Label('Asset Categories'),
                        dbc.Dropdown(id='asset-categories',
                                      options=[{'label': i, 'value': i} for i in master_categories],
                                      value=[i for i in tags],
                                      multi=True)
                        ]),
                    
                    dbc.FormGroup([
                        dbc.Label('Asset Description'),
                        dbc.Input(id='asset-desc', type='text', placeholder='Description')
                        ]),
                    
                    dbc.FormGroup([
                        dbc.Label('Asset Website'),
                        dbc.Input(id='asset-website', type='url', placeholder='Website')
                        ]),
                    
                    dbc.Button('submit-asset-button'),
                    
                    html.Div(id='submit-asset-confirmation'),
                    
                    ]),
                
                
                # Map on which users can click a point to add an asset
                dl.Map([dl.TileLayer(), dl.LayerGroup(id='layer')],
                       id="submit-asset-map"),
                
                html.P('Click on map to enter the exact coordinate of the asset:'),
                html.Div(id='coordinate_click_id')
                
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