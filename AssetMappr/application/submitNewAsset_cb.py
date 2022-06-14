"""
File: submitNewAsset_cb.py
Author: Mihir Bhaskar

Desc: This file creates the callbacks which interact with the submitNewAsset popup
      
      This is linked to the submitNewAsset.py layout file, as well as the submitNewAsset_db
      file in the Database folder, which writes the new user-entered asset info to the database

Input: 
    app: an initialized dash app
    df: data frame with loaded assets
    asset_categories: data frame with asset-category mappings
    
Output: 
    Callbacks relating to the submit-new-asset feature
     
"""
import dash
from dash.dependencies import Input, Output, State
import dash_leaflet as dl
import uuid
from flask import request
import dash_bootstrap_components as dbc
import requests
import json
import pandas as pd



from AssetMappr.database.submitNewAsset_db import submitNewAsset_db

def submitNewAsset_cb(app):
    
    # Callbacks for each of the sub-modals, to control when it opens/closes
    # The modals are connected with back/next buttons, which determine when each one is open/close
    
    # Modal 1 callback (the first thing that opens when the user clicks submit new asset)
    @app.callback(
        Output('modal-1', 'is_open'),
        [Input('open-asset-submit', 'n_clicks'),
         Input('back-modal-1', 'n_clicks'),
         Input('open-modal-2', 'n_clicks')            
        ],
        [State('modal-1', 'is_open')]
        )
    def toggle_modal_1(n0, n1, n2, is_open):
        if n0 or n1 or n2:
            return not is_open
        return is_open
    
    # Modal 2 callback (opens when the user clicks next from modal 1 or back from modal 3)
    @app.callback(
        Output('modal-2', 'is_open'),
        [Input('open-modal-2', 'n_clicks'),
         Input('back-modal-1', 'n_clicks'),
         Input('back-modal-2', 'n_clicks'),
         Input('open-modal-3', 'n_clicks')
        ],
        [State('modal-2', 'is_open')]
        )
    def toggle_modal_2(n0, n1, n2, n3, is_open):
        if n0 or n1 or n2:
            return not is_open
        return is_open
    
    # Modal 3 callback (opens when the user clicks next from modal 2 or back from modal 4)
    @app.callback(
        Output('modal-3', 'is_open'),
        [Input('open-modal-3', 'n_clicks'),
         Input('back-modal-2', 'n_clicks'),
         Input('back-modal-3', 'n_clicks'),
         Input('open-modal-4', 'n_clicks')
        ],
        [State('modal-3', 'is_open')]
        )
    def toggle_modal_3(n0, n1, n2, n3, is_open):
        if n0 or n1 or n2 or n3:
            return not is_open
        return is_open

    # Modal 4 callback (opens when the user clicks next from modal 3)
    @app.callback(
        Output('modal-4', 'is_open'),
        [Input('open-modal-4', 'n_clicks'),
         Input('back-modal-3', 'n_clicks'),
        ],
        [State('modal-4', 'is_open')]
        )
    def toggle_modal_4(n0, n1, is_open):
        if n0 or n1:
            return not is_open
        return is_open
    
    # Callback to render the Leaflet map on which users will pin the location of the asset
    @app.callback(
        Output('submit-asset-map', 'children'),
        Input('modal-2', 'is_open'),
        Input('selected-community-info', 'data')
        )
    def render_map_on_show(is_open, selected_community):
        # This ensures that the map only renders if modal 2 is open, preventing screen resizing issues
        if is_open:
            
            # Get the lat-long to center on when the map loads
            selected_community = pd.read_json(selected_community, orient='split')
            community_center_lat = float(selected_community['latitude'])
            community_center_lon = float(selected_community['longitude'])

            
            return dl.Map([dl.TileLayer(), dl.LayerGroup(id='layer')],
                      id='submit-asset-map', 
                      # TODO: automate the centering of the map based on user input on community
                      zoom=14, center=(community_center_lat, community_center_lon),
                      style={'width': '100%', 'height': '65vh', 'margin': "auto", "display": "block"}
                     )
    
    # Callback to display the marker point where the user has clicked on the map
    @app.callback(Output('layer', 'children'), [Input('submit-asset-map', 'click_lat_lng')])
    def map_click(click_lat_lng):
        return [dl.Marker(position=click_lat_lng, children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng)))]
    
    # Callback to zoom into the text inputted address, using geocoding
    @app.callback(
        
        # Outputs the new centering/zoom location directly on the map
        # The zoom-address-confirmation output is a box that will display nothing
        # if the address geocoding worked, but an error message if it didn't work
        Output('zoom-address-confirmation', 'children'),
        Output('submit-asset-map', 'center'),
        Output('submit-asset-map', 'zoom'),
        Output('address-search', 'value'), # this is to clear the value in the search box once submitted
        [Input('search-address-button', 'n_clicks')],
        [State('address-search', 'value')],
        [State('selected-community-info', 'data')]
        )
    def zoom_to_address(n_clicks, address_search, selected_community):
        if n_clicks == 0:
            return ''
        else:
            # Geocode the lat-lng using Google Maps API
            google_api_key = 'AIzaSyDitOkTVs4g0ibg_Yt04DQqLaUYlxZ1o30'
            
            # Retrieve the name of the community to add to the geocoding search to make it more accurate
            selected_community = pd.read_json(selected_community, orient='split')
            
            community_name = selected_community['community_name'][1]
                        
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
        Output('clicked-address', 'children'),
        Input('submit-asset-map', 'click_lat_lng')
        )
    def geocoded_clicked_ltlng(click_lat_lng):
        
        # Geocode the lat-lng using Google Maps API
        google_api_key = 'AIzaSyDitOkTVs4g0ibg_Yt04DQqLaUYlxZ1o30'
        
        params = {'key': google_api_key,
                  'latlng': '{},{}'.format(click_lat_lng[0], click_lat_lng[1])}
        
        url = 'https://maps.googleapis.com/maps/api/geocode/json?'
        
        response = requests.get(url, params)
        result = json.loads(response.text)
        
        # Getting the formatted address from the JSON return
        global address
        address = result['results'][0]['formatted_address']
        
        return 'Selected address: {}'.format(address)

    # Callback to take all the user-submitted info on the new asset, write it to the database, and reset the form
    @app.callback(
        
        # The output displays a confirmation message, and resets the values of all the input fields to blank/None
        Output(component_id='submit-asset-confirmation', component_property='children'),
        Output('user-name', 'value'),
        Output('user-role', 'value'),
        Output('asset-name', 'value'),
        Output('asset-categories', 'value'),
        Output('asset-desc', 'value'),
        Output('asset-website', 'value'),
        
        # The inputs of the text boxes and the lat long are all state-dependent on clicking the submit button
        [Input('submit-asset-button', 'n_clicks')],
        [State('user-name', 'value')],
        [State('user-role', 'value')],
        [State('asset-name', 'value')],
        [State('asset-categories', 'value')],
        [State('asset-desc', 'value')],
        [State('asset-website', 'value')],
        [State('submit-asset-map', 'click_lat_lng')],
        [State('selected-community-info', 'data')]
        )
    def store_submitted_info(n_clicks, user_name, user_role, name, categories, 
                             desc, site, click_lat_lng, selected_community):
        
        # If the 'Submit' button has not been clicked yet, return or do nothing
        if n_clicks == 0:
            return ''
        # If the submit button has been clicked, then write the info to the DB
        else:
            # Get the IP address from which this callback request was generated
            ip = request.remote_addr

            # Create a staged asset ID            
            staged_asset_id = str(uuid.uuid4()) 
            
            # Extract the selected commmunity_geo_id
            selected_community = pd.read_json(selected_community, orient='split')
            community_geo_id = int(selected_community['community_geo_id'])

            # Feed the info into the database-write function, which writes to SQL (found in database folder)
            submitNewAsset_db(staged_asset_id, ip, user_name, user_role, name, categories, desc, 
                              site, click_lat_lng, community_geo_id, address=address)
            
            # Note: all the code below is an attempt to append this staged asset to the DF temporarily. Need to explore
            # A different solution later, for now commenting everything out
            
            # Writing the asset to the temporary data frame used by the app, so the user can see this uploaded asset
            # in their current session. Note: this is over and above writing it to the actual postgreSQL DB, which happens
            # above
            
            # # Appending the information to a new row in df_copy
            # new_df_row = {'asset_id': staged_asset_id, 'asset_name': name,
            #            'asset_status': 'Staged', 'community_geo_id': 123,
            #            'source_type': 'User', 'description': desc, 'website': site,
            #            'latitude': click_lat_lng[0], 'longitude': click_lat_lng[1]}
            # df_copy = df_copy.append(new_df_row, ignore_index=True)
            
            # # Appending the category information to new row(s) in asset_categories_copy
            # for cat in categories:
            #     new_cat_row = {'asset_id': staged_asset_id, 'category': cat}
            #     asset_categories_copy = asset_categories_copy.append(new_cat_row, ignore_index=True)
            
            # # This global part ensures that we write these changes to the global versions of df and asset_categories,
            # # that can be accessed by the rest of the application (e.g. the showMap functions)
            # global df, asset_categories
            # df, asset_categories = df_copy, asset_categories_copy
     
            # Returns user confirmation, and empty strings/None types to the corresponding Input boxes
            return (dbc.Alert('''{} submited successfully!  
                   Thank you for helping out.'''.format(name), dismissable=True, color='success'),
                   
                   '', '', '', None, '', ''
                   
                   )
            