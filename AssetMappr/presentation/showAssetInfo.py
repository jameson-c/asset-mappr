"""
File: showAssetInfo.py
Author: Mihir Bhaskar, Anna Wang

Desc: This file returns an HTML Div with information about the selected asset on the asset map

These elements take inputs from showAssetInfo_cb in the application folder

Output: 
    - HTML Div, called in makeLayout()
"""
from dash import html

def showAssetInfo():
    return html.Div([
                html.H6(id='display-asset-name'),
                
                html.H6(id='display-asset-desc'),
                
                html.H6('Website:'),                
                html.Pre(id='web_link'),
            ])
