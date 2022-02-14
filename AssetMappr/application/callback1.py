"""
File: callback1.py
Author: Mihir Bhaskar, Anna Wang, Jameson Carter

Desc: This file manages the callback which dynamically updates the database
      containing asset information. 
Input: 
    google_apikey: A google API key- str
    path: The path to the database MainFrame.csv- str
    app: an initialized dash app
Output: 
    Updates the database Mainframe.csv directly. 
"""

# =============================================================================
# Importing functions, libraries and set-up
# =============================================================================

# Libraries
from dash.dependencies import Input, Output, State
import pandas as pd
import os, sys

google_apikey = 'AIzaSyDitOkTVs4g0ibg_Yt04DQqLaUYlxZ1o30'

path = 'C:/Users/jacar/OneDrive/Documents/asset-mappr/AssetMappr/database/MainFrame.csv'

df = pd.read_csv(path, index_col=0)
# This gets the time of the most recent content modification -> when the data is first loaded into the app
lastmt = os.stat(path).st_mtime

def update_csv(app):
# =============================================================================
# Callback for the dataset to be updated when the .csv is modified (by data entry)
# =============================================================================

# Data update callback
    @app.callback(Output('placeholder', 'children'), 
              [Input('data-update-interval', 'n_intervals')]
              )
    def dataset_update_trigger(n):
    
        # Reading in the data fresh if there was an update, and update last modified time
        global lastmt # lastmt and df have to be defined as global variables in order to hold outside of this function
                  # and be relevant for the next callback, which filters/uses the dataset
        global df
        
        if os.stat(path).st_mtime > lastmt:
            lastmt = os.stat(path).st_mtime
            df = pd.read_csv(path)
            return ""
        return ""