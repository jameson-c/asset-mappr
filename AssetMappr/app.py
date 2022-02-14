"""
File: app.py
Author: Mihir Bhaskar, Anna Wang, Jameson Carter

Desc: This file initializes the Dash app
"""

# =============================================================================
# Importing functions, libraries and set-up
# =============================================================================
import dash
import sys, os


# Automatically set directories to the application and presentation folders
# CHANGE THIS to wherever your filepath is
path = 'C:\\Users\\jacar\\OneDrive\\Documents\\asset-mappr\\AssetMappr'
sys.path.append(os.path.join(path, "application"))
import callback1 
import callback2 
import callback3 

sys.path.append(os.path.join(path, "presentation"))
import layout

# =============================================================================
# Initialize app
# =============================================================================  
if __name__ == '__main__':
    
    app = dash.Dash(__name__)
    app.title = 'Steel City Services'
    
    app.layout = layout.make_layout()
    callback1.update_csv(app)
    callback2.get_filtered_results(app)
    callback3.data_entry(app)
    
    app.run_server(debug=True, dev_tools_hot_reload=False)

