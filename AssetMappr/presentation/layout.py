"""
File: layout.py
Author: Mihir Bhaskar, Anna Wang, Jameson Carter

Desc: This file creates the main home page layout of the app
Input: 
    - Draws on the individual layout components, defined in separate .py files
    in the 'presentation' folder
    - df: the main assets data frame loaded in
    - master_categories: the unique list of possible category values
    - tagList: the unique list of possible value tags
    - asset_categories: data frame with assets and their catagories
    
    
Output:
    - A function called makeLayout() that returns the layout section of the Dash app,
    which is called in the app.py file
"""
# =============================================================================
# Imports
# =============================================================================

from dash import dcc
from dash import html
import dash_bootstrap_components as dbc


# Importing all the layout components
from AssetMappr.presentation.showMap import showMap
from AssetMappr.presentation.showAssetInfo import showAssetInfo
from AssetMappr.presentation.submitRating import submitRating
from AssetMappr.presentation.submitNewAsset import submitNewAsset
from AssetMappr.presentation.suggestMissingAsset import suggestMissingAsset
from AssetMappr.presentation.showMap_Planner import showMap_Planner
from AssetMappr.presentation.showCheckbox import showCheckbox

# =============================================================================
# Function
# =============================================================================


def makeLayout(df, master_categories, tagList_pos, tagList_neg, asset_categories):

    return html.Div([

        # Layout is split into two overall tabs
        dcc.Tabs([

            # Tab 1: Page to view, rate, and upload assets
            dcc.Tab(id='tab1', label='Tell us about your community', children=[

                # This tab uses a grid structure of rows and columns

                # Row 1
                # dbc.Row([
                #     dbc.Col(
                #         html.H4(
                #             'Use the map below to view and select assets', id='useTheMap'),
                #     ),
                # ]),

                # Row 2
                dbc.Row([
                    dbc.Col([
                        # Outputs an option to select categories
                        showCheckbox(master_categories),
                        # Displays the function to submit new assets
                        html.H6(
                            'Know about an asset we don\'t have? Tell us about it! \U0001f447', id='know'),
                        submitNewAsset(master_categories)],width=3),
                    # the map displaying assets 
                    dbc.Col(showMap(), width=5),
                    dbc.Col([
                        showAssetInfo(master_categories),
                        # Displays the functionality to rate the selected asset
                        submitRating(tagList_pos),
                        html.Br(),
                    ], width=4),
                ], className="g-0"),
            ]),

            # Tab 2: Page to suggest 'missing' assets, share other thoughts about community dev
            dcc.Tab(id='tab2', label='What are your hopes for the future?', children=[
                suggestMissingAsset(master_categories),
            ]),

            # Tab 3: Page to planner view (name is tbd)
            dcc.Tab(id='tab3', label='Planner View', children=[
                showMap_Planner()
            ]),

        ]),
    ])
