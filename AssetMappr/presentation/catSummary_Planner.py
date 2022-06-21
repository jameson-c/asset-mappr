"""
File: catSummary_Planner.py
Author: Anna Wang, Mihir Bhaskar

Desc: This file returns an HTML Div with the category summary bar chart

The main bar chart is created in catSummary_Planner_cb in the application folder

Input

Output:
    - HTML Div, called in makeLayout()
"""

from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from AssetMappr.presentation.showAssetInfo_Planner import showAssetInfo_Planner
import plotly.express as px

def catSummary_Planner():
    return html.Div([
        
        html.H5('What type of category-wise summary would you like to see?'),
        
        html.H6('Select statistic:'),
        
        dcc.Dropdown(
            id='choose-the-stat',
            options=[
                {"label": "Number of existing assets", "value": 'count_number'},
                {"label": "Average of all ratings for assets", "value": 'rating_avg'},
                {"label": "Number of suggested (missing) assets", "value": 'num_missing'}             
                ],
            value='count_number',
            multi=False
        ),

        dcc.Graph(id='bar-chart-for-planner')

        ])