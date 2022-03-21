"""
File: display_table.py
Author: Mihir Bhaskar

Desc: This file creates the main displayed data table
Input: 
   - Is linked to a callback called display_table_cb that sits in the application folder
   - The link is by the id 'main-table'

Output: 
    - A function that returns an HTML Div containing the main table output
    
"""
import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc


def display_table():

    return html.Div(id='main-table')
