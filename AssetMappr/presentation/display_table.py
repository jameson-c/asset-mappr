"""
File: display_table.py
Author: Mihir Bhaskar

Desc: This file creates the main displayed data table
Input: 
   - The return from a callback that is a pandas dataframe
   - The corresponding callback that gives this return is display_table_cb

Output: 
    - A function that returns an HTML Div containing the user new asset upload
    
"""
import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import dcc
from dash import html

def display_table():
    
    return html.Div(id='main-table')



