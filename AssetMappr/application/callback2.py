"""
File: callback2.py
Author: Mihir Bhaskar, Anna Wang, Jameson Carter

Desc: This file reacts to user query of the database
Input: 
    google_apikey: A google API key- str
    path: The path to the database MainFrame.csv- str
    app: an initialized dash app
    tags: a list of asset categories- str

Output: 
    Returns a version of the data according to user's query. 
"""

# =============================================================================
# Importing functions, libraries and set-up
# =============================================================================

# Programs defined in this repo:
from getAddressCoords import getAddressCoords
from filterNearby import filterNearby

# Other libraries
import dash
from dash import dash_table
from dash.dependencies import Input, Output, State
import pandas as pd

google_apikey = 'AIzaSyDitOkTVs4g0ibg_Yt04DQqLaUYlxZ1o30'

path = 'MainFrame.csv'

df = pd.read_csv(path, index_col=0)

# Pulling column names from df to serve as options to populate the dropdown
tags = ['CLOTHING', 'FOOD', 'HOUSEHOLD GOODS', 'HOUSING', 'TRAINING AND OTHER SERVICES']

# =============================================================================
# Callback for the filtered set of results to be created and displayed
# =============================================================================

def get_filtered_results(app):

    @app.callback(
        Output(component_id='output-table', component_property='children'),
       [Input('submit-user-address', 'n_clicks')],
       [State('user-address', 'value')],
       Input('max-travel-dist', 'value'),
       Input('asset-type', 'value'),
    )
    def search_output_div(n_clicks, user_address, max_travel_dist, asset_type):
        # First output value, before user has submitted anything - show blank
        if n_clicks == 0:
            return ''
        
        else:
            # Translate input address into lat-longs 
            user_coords = getAddressCoords(input_address = user_address, api_key = google_apikey)
            
            # Check if address was translated properly - if yes, it should return a tuple
            if type(user_coords) == list:
        
                # =============================================================================
                # Filtering the data according to parameters            
                # =============================================================================
                
                # Filter the data frame with observations that fall within max distance limit, using a user-defined program
                fdata = filterNearby(point = user_coords[0], data = df, max_dist = max_travel_dist)
                
                # Now filter this data with only the categories the user selected
                
                # First step: create a flag variable that takes 1 if any of the relevant categories have '1' 
                fdata['Keep'] = 0
                
                # Asset_type is a list of categories that users have selected
                for i in asset_type:
                    fdata.loc[fdata[i] == 1, 'Keep'] = 1
                    
                # Keep the appropriate rows
                fdata = fdata[fdata['Keep'] == 1]
        
                # =============================================================================
                # Format the data for presenting it in the front-end table            
                # =============================================================================
                
                # Combine the information in dummy columns to one column with comma-separated services provided
                fdata['SUPPORT PROVIDED'] = ''
        
                for i in tags: # Note: tags is defined at the top of the script, as the list of service categories
                    fdata.loc[fdata[i] == 1, 'SUPPORT PROVIDED'] += i + ',' # Concat on the service name (column name) if it's value is 1
                fdata['SUPPORT PROVIDED'] = fdata['SUPPORT PROVIDED'].str[:-1] # Strip the last comma 
                
                # Round the distance in miles column to 2 decimal places
                fdata['DISTANCE IN MILES'] = fdata['DISTANCE IN MILES'].round(2)
                
    
                # To-do: Make the vicinity a 'link' display that when users click gives them directions
                # Link format to follow: https://www.google.com/maps/dir/?api=1&origin=760+West+Genesee+Street+Syracuse+NY+13204&destination=314+Avery+Avenue+Syracuse+NY+13204
                # How to do it in code: https://github.com/plotly/dash-table/issues/222#issuecomment-585179610
                
                # Select the appropriate columns to display
                fdata = fdata[['NAME', 'SUPPORT PROVIDED', 'VICINITY', 'DISTANCE IN MILES', 'WEBSITE', 'NOTES']]
                                        
                # Convert the dataframe into Dash's DataTable for display in the app
                tmpdta = fdata.to_dict('rows')
                tmpcols = [{"name": i, "id": i,} for i in (fdata.columns)]
                
                # Return a well-formatted dash table
                return dash_table.DataTable(data = tmpdta, columns = tmpcols,
                                            fixed_rows={'headers': True},
                                            #fill_width=False,
                                            # Need to play around with this code
                                             style_cell_conditional=[
                                                 {'if': {'column_id': 'DISTANCE IN MILES'},
                                                  'width':'80px'}],
                                            #     {'if': {'column_id': 'support provided'},
                                            #      'width': '20%'},
                                            #     {'if': {'column_id': 'vicinity'},
                                            #      'width':'30%'},
                                            #     {'if': {'column_id': 'distance in miles'},
                                            #      'width': '10%'},
                                            #     ],
                                            style_data={'whiteSpace':'normal',
                                                        'height': 'auto',
                                                        'lineHeight':'15px'},
                                            style_cell={'textAlign': 'left',
                                                        'height': 'auto',
                                                        'minWidth': '80px',
                                                        'width': '180px',
                                                        'maxWidth': '180px',
                                                        'whiteSpace': 'normal'},
                                            style_header={'fontWeight':'bold'})
                
            # If address failed, return the string error message
            else:
                return "Invalid address" ''

