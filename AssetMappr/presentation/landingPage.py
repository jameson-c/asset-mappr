"""
File: landingPage.py
Author: Mihir Bhaskar

Desc: This file returns an HTML Div with the content of the landing or welcome page

Output: 
    - HTML Div with the main welcome page content. This is called directly in the app.py file
"""
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc


def makeLandingPage(master_communities):

    return html.Div(className='landing', children=[
        html.H1('Welcome to AssetMappr!', style={
                'color': '#2C3E50'}, id="Welcome"),
        html.Br(),
        html.H4('''We are a group of students that believe in the power of community participation. 
                    We hope that our app will make it easier for you to share your thoughts about the assets in your community,
                    helping planners make better investments for the future.''', id="WelWords"),
        html.Br(),
        html.H5('Select your community from the dropdown below, and the click the button to enter the app'),
        dcc.Dropdown(id='community-select',
                        options=[{'label': master_communities.loc[master_communities.index[i], 'community_name'], 
                                  'value': master_communities.loc[master_communities.index[i], 'community_geo_id']} 
                                  for i in range(len(master_communities))],
                        value=None,
                        multi=False),

        # Link to take users to the main home page of the app
        dbc.Button('Enter the app',
                   href='/home', id="enterButton", n_clicks=0)
    ])
