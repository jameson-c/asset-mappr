"""
File: catSummary_Planner.py
Author: Anna Wang, Mihir Bhaskar

Desc: This file returns an HTML Div with the category summary bar chart component of the planner dashboard

The main bar chart is created in catSummary_Planner_cb in the application folder, because it adapts to the input
on what the user wants to see

Output:
    - HTML Div, called in makeLayout()
"""
from dash import dcc
from dash import html


def catSummary_Planner():
    return html.Div([

        # Graph component to hold the graph created in the callback
        # dcc.Graph(id='bar-chart-for-planner')

        ])