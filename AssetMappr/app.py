"""
File: app.py
Author: Mihir Bhaskar, Anna Wang, Jameson Carter

Desc: This file initializes the Dash app
"""

# =============================================================================
# Importing functions, libraries and set-up
# =============================================================================
import dash
from layout import make_layout
from callback1 import update_csv
from callback2 import get_filtered_results
from callback3 import data_entry

# =============================================================================
# Initialize app
# =============================================================================  
if __name__ == '__main__':
    
    app = dash.Dash(__name__)
    app.title = 'Steel City Services'
    app.layout = make_layout()
    update_csv(app)
    get_filtered_results(app)
    data_entry(app)
    
    app.run_server(debug=True, dev_tools_hot_reload=False)

