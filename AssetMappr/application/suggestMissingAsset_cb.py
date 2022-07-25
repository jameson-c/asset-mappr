"""
File: suggestMissingAsset_cb.py
Author: Mihir Bhaskar

Desc: This file creates the callbacks which interact with the suggest_missing_asset popup
      
      This is linked to the suggestMissingAsset.py layout file, as well as the suggestMissingAsset_db
      file in the Database folder, which writes the new user-entered info to the database

Input: 
    app: an initialized dash app
    
Output: 
    Callbacks relating to the suggest_missing_asset feature
     
"""
import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import dcc
from dash import html
import pandas as pd
import dash_leaflet as dl
import dash_bootstrap_components as dbc
import pandas as pd
import json
import requests
import os


from flask import request

from AssetMappr.database.suggestMissingAsset_db import suggestMissingAsset_db

def suggestMissingAsset_cb(app):
    
    # Callbacks for each of the sub-modals, to control when it opens/closes
    # The modals are connected with back/next buttons, which determine when each one is open/close
    
    # Modal 1 callback (the first thing that opens when the user clicks submit new asset)
    @app.callback(
        Output('modal-1-missing', 'is_open'),
        [Input('open-suggest-missing-submit', 'n_clicks'),
         Input('back-modal-1-missing', 'n_clicks'),
         Input('open-modal-2-missing', 'n_clicks')            
        ],
        [State('modal-1-missing', 'is_open')]
        )
    def toggle_modal_1_missing(n0, n1, n2, is_open):
        if n0 or n1 or n2:
            return not is_open
        return is_open
    
    # Modal 2 callback (opens when the user clicks next from modal 1 or back from modal 3)
    @app.callback(
        Output('modal-2-missing', 'is_open'),
        [Input('open-modal-2-missing', 'n_clicks'),
         Input('back-modal-1-missing', 'n_clicks'),
         Input('back-modal-2-missing', 'n_clicks'),
         Input('open-modal-3-missing', 'n_clicks')
        ],
        [State('modal-2-missing', 'is_open')]
        )
    def toggle_modal_2_missing(n0, n1, n2, n3, is_open):
        if n0 or n1 or n2:
            return not is_open
        return is_open
    
    # Modal 3 callback (opens when the user clicks next from modal 2 or back from modal 4)
    @app.callback(
        Output('modal-3-missing', 'is_open'),
        [Input('open-modal-3-missing', 'n_clicks'),
         Input('back-modal-2-missing', 'n_clicks'),
         Input('back-modal-3-missing', 'n_clicks'),
         Input('open-modal-4-missing', 'n_clicks')
        ],
        [State('modal-3-missing', 'is_open')]
        )
    def toggle_modal_3_missing(n0, n1, n2, n3, is_open):
        if n0 or n1 or n2 or n3:
            return not is_open
        return is_open

    # Modal 4 callback (opens when the user clicks next from modal 3)
    @app.callback(
        Output('modal-4-missing', 'is_open'),
        [Input('open-modal-4-missing', 'n_clicks'),
         Input('back-modal-3-missing', 'n_clicks'),
        ],
        [State('modal-4-missing', 'is_open')]
        )
    def toggle_modal_4_missing(n0, n1, is_open):
        if n0 or n1:
            return not is_open
        return is_open
    
    # Callback to render the Leaflet map on which users will pin the location of the missing asset
    @app.callback(
        Output('submit-missing-asset-map', 'children'),
        Input('modal-2-missing', 'is_open'),
        Input('selected-community-info', 'data')
        )
    def render_map_on_show(is_open, selected_community):
        # This ensures that the map only renders if the modal is open, preventing screen resizing issues
        if is_open:
            
            # Get the lat-long to center on when the map loads
            selected_community = pd.read_json(selected_community, orient='split')
            community_center_lat = float(selected_community['latitude'])
            community_center_lon = float(selected_community['longitude'])

            return dl.Map([dl.TileLayer(), dl.LayerGroup(id='missing-layer')],
                      id='submit-missing-asset-map', 
                      # TODO: automate the centering of the map based on user input on community
                      zoom=14, center=(community_center_lat, community_center_lon),
                      style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}
                     )
    
    # Callback to display the point the user has clicked on the map
    @app.callback(Output('missing-layer', 'children'), [Input('submit-missing-asset-map', 'click_lat_lng')])
    def map_click(click_lat_lng):
        return [dl.Marker(position=click_lat_lng, children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng)))]
        
    # Callback to zoom into the text-inputted search address, using geocoding
    @app.callback(
        
        # Outputs the new centering/zoom location directly on the map
        # The zoom-address-confirmation output is a box that will display nothing
        # if the address geocoding worked, but an error message if it didn't work
        Output('zoom-address-confirmation-missing', 'children'),
        Output('submit-missing-asset-map', 'center'),
        Output('submit-missing-asset-map', 'zoom'),
        Output('address-search-missing', 'value'), # this is to clear the value in the search box once submitted
        [Input('search-address-button-missing', 'n_clicks')],
        [State('address-search-missing', 'value')],
        [State('selected-community-info', 'data')]
        )
    def zoom_to_address_missing(n_clicks, address_search, selected_community):
        if n_clicks == 0:
            return ''
        else:
            # Geocode the lat-lng using Google Maps API
            google_api_key = os.getenv('GOOGLE_API_KEY')
            
            # Retrieve the name of the community to add to the geocoding search to make it more accurate
            selected_community = pd.read_json(selected_community, orient='split')
            
            community_name = selected_community['community_name'].values.tolist()[0]
            
            # Adding place name to make the search more accurate (to generalize)
            address_search = address_search + ' ' + community_name + ', PA'
            community_center_lat = float(selected_community['latitude'])
            community_center_lon = float(selected_community['longitude'])
            
            params = {'key': google_api_key,
                      'address': address_search}
            
            url = 'https://maps.googleapis.com/maps/api/geocode/json?'
            
            response = requests.get(url, params)
            result = json.loads(response.text)

            # Check these error codes again - there may be more
            if result['status'] not in ['INVALID_REQUEST', 'ZERO_RESULTS']:
                
                lat = result['results'][0]['geometry']['location']['lat']
                long = result['results'][0]['geometry']['location']['lng']

                # Return the error message, lat-long to center on, and amount of zoom
                return ('', (lat, long), 20, '')
                        
            else:
                return ('Invalid address; try entering', (community_center_lat, community_center_lon), 14, address_search)



    # Callback to display the geocoded address based on the clicked lat long
    @app.callback(
        Output('clicked-address-missing-asset', 'children'),
        Input('submit-missing-asset-map', 'click_lat_lng')
        )
    def geocoded_clicked_ltlng_missing(click_lat_lng):
        
        # Geocode the lat-lng using Google Maps API
        google_api_key = os.getenv('GOOGLE_API_KEY')
        
        params = {'key': google_api_key,
                  'latlng': '{},{}'.format(click_lat_lng[0], click_lat_lng[1])}
        
        url = 'https://maps.googleapis.com/maps/api/geocode/json?'
        
        response = requests.get(url, params)
        result = json.loads(response.text)
        
        # Getting the formatted address from the JSON return
        global address_missing
        address_missing = result['results'][0]['formatted_address']
        
        return 'Selected address: {}'.format(address_missing)


    # Callback to take all the user-submitted info on the missing asset, write it to the database, and reset the form
    @app.callback(
        
        # The output displays a confirmation message, and resets the values of all the input fields to blank/None
        Output(component_id='submit-suggestion-confirmation', component_property='children'),
        Output('missing-user-name', 'value'),
        Output('missing-user-role', 'value'),
        Output('missing-asset-name', 'value'),
        Output('missing-asset-categories', 'value'),
        Output('missing-asset-desc', 'value'),
        Output('missing-asset-justification', 'value'),
        Output('clicked-address-missing-asset', 'value'),
        
        # The inputs of the text boxes and the lat long are all state-dependent on clicking the submit button
        [Input('submit-suggestion-button', 'n_clicks')],
        [State('missing-user-name', 'value')],
        [State('missing-user-role', 'value')],
        [State('missing-asset-name', 'value')],
        [State('missing-asset-categories', 'value')],
        [State('missing-asset-desc', 'value')],
        [State('missing-asset-justification', 'value')],
        [State('submit-missing-asset-map', 'click_lat_lng')],
        [State('selected-community-info', 'data')]
        )
    def store_submitted_info(n_clicks, user_name, user_role, name, categories, 
                             desc, justification, click_lat_lng, selected_community):
        # If the 'Submit' button has not been clicked yet, return or do nothing
        if n_clicks == 0:
            return ''
        # If the submit button has been clicked, then write the info to the DB
        else:
            # Get the IP address from which this callback request was generated
            ip = request.remote_addr
    
            # Extract the selected commmunity_geo_id
            selected_community = pd.read_json(selected_community, orient='split')
            community_geo_id = int(selected_community['community_geo_id'])

            # Write to the database
            suggestMissingAsset_db(ip, user_name, user_role, name, categories, desc, click_lat_lng, 
                                   justification, address_missing, community_geo_id)
                        
            # Returns user confirmation, and empty strings/None types to the corresponding Input boxes
            return (dbc.Alert('''Suggestion for {} submited successfully! Thank you for helping out.'''.format(name), 
                              dismissable=True, color='success'),
                       
                       '', '', '', None, '', '', ''
                       
                       )
            
