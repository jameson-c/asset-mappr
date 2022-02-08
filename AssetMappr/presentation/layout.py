"""
File: layout.py
Author: Mihir Bhaskar, Anna Wang, Jameson Carter

Desc: This file establishes content controls and descriptions for the layout
Input: 
    tags: a list of asset categories- str

Output: 
    Returns a version of the data according to user's query. 
"""
# =============================================================================
# Importing functions, libraries and set-up
# =============================================================================

# Other libraries
import os
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import tkinter
from tkinter import *
from tkinter import ttk
import tkinter.messagebox

# Pulling column names from df to serve as options to populate the dropdown
tags = ['CLOTHING', 'FOOD', 'HOUSEHOLD GOODS', 'HOUSING', 'TRAINING AND OTHER SERVICES']

# =============================================================================
# Defining functions to create the appropriate HTML Divs (i.e. sections of the UI)
# =============================================================================

def description_card():
    """
    Returns
    -------
    A Div containing dashboard title & descriptions
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Steel City Services"),
            html.H4('Test header')
            html.H3("Find and contribute support options near you"),
            html.Div(
                id="intro",
                children='''Use the search options below to find locations near you providing support, or
                            let us know about an initiative we may have missed.''',
                ),
            ],
        )

def generate_control_card():
    """

    Returns
    -------
    A Div containing the user-defined options for searching and adding new info

    """
    return html.Div(
        id="control-card",
        children=[
            # Entering address
            html.P("Enter your address and click submit"),
            dcc.Input(id='user-address', value='', type='text'),
            html.Button('Submit', id='submit-user-address', n_clicks = 0),
            html.Br(),
            html.Br(),
            # Entering distance
            html.P("Enter your max travel distance in miles"),
            dcc.Input(id='max-travel-dist', value=10, type='number'),
            html.Br(),
            html.Br(),
            # Selecting categories
            html.P("Select relevant categories"),
            dcc.Dropdown(
            id='asset-type',
            options=[{'label': i, 'value': i} for i in tags],
            value=[i for i in tags],
            multi=True
            ),
            html.Br(),
            # Button to update data
            html.P("Know a place we don't? Click to add info"),
            html.Button('Submit your own data', id='submit-data'),
            html.Div(id='output-container-button'),
            
            # Interval with which data gets updated
            dcc.Interval(id='data-update-interval', interval=1000, n_intervals=0),
            html.P(id='placeholder')
            
            
            ]
        
        )
    
# =============================================================================
# Defining layout of the app
# =============================================================================

def make_layout():
    return html.Div([
    
        # Left column
        html.Div(id="left-column",
             className="four columns",
             children=[description_card(), generate_control_card()]
             ),
    
        # Right column
        html.Div(
            id="right-column",
            className="eight columns",
            children=[
                # Output table
                html.Div(id='output-table'), 
                ],
            ),
        ],
        )