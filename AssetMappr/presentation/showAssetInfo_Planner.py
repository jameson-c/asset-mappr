"""
File: showAssetInfo_Planner.py
Author: Anna Wang

Desc: This file returns an HTML Div with information about the selected asset on the asset map in planner views

These elements take inputs from showAssetInfo_Planner_cb in the application folder

Output: 
    - HTML Div, called in makeLayout()
"""
from dash import html


def showAssetInfo_Planner():
    return html.Div([
        html.H6(id='name'),

        html.H6(id='desOrScore'),

        html.H6(id='justificationOrComments'),

        html.H6(id='address'),
    ])
