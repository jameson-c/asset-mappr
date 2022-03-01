"""
File: layout.py
Author: Mihir Bhaskar, Anna Wang, Jameson Carter

Desc: This file creates the main layout of the app
Input: 
    - Draws on the individual layout components, defined in separate .py files
    in the 'presentation' folder
    
Output:
    - A function called make_layout() that returns the layout section of the Dash app
    
"""
import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import dcc
from dash import html


from AssetMappr.presentation.title_desc import title_desc
from AssetMappr.presentation.submit_new_asset import submit_new_asset 
from AssetMappr.presentation.display_table import display_table

# =============================================================================
# Function that makes the layout of the app
# =============================================================================
def make_layout():
    return html.Div([
        dcc.Tabs([
            
            # Tab 1: Home page/view assets
            dcc.Tab(label='Community User View', children=[
                
                title_desc(),
                
                display_table(),
                
                submit_new_asset()

                
                ]),
            
            # Tab 2: Add asset
            dcc.Tab(label='Planner View', children=[
                
                html.H5("Placeholder")
                
                ])
            
            ]),
        
        
        
        # Interval for data update
        dcc.Interval(id='interval_pg', interval=1000, n_intervals=0)
        
    
        ])

