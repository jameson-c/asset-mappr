"""
File: display_table_cb.py
Author: Mihir Bhaskar, Anna Wang

Desc: This file creates the callback which fetches the database from the server
      and returns a Dash Data Table displaying it.
      
      This is linked to the display_table.py layout file, through the output id 'main-table'

Input: 
    db: The database object
    app: an initialized dash app
Output: 
    A callback that returns a Dash Data Table with the SQL data 
"""
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import html
from collections import OrderedDict
import pandas as pd


def display_table_cb(app, db):

    @app.callback(Output('main-table', 'children'),
                  [Input('interval_pg', 'n_intervals')])
    def populate_datatable(n_intervals):
        df = pd.read_sql_table('assets', con=db.engine)

        return dash_table.DataTable(id='main_table',
                                    columns=[{'name': str(x), 'id': str(x)}
                                             for x in df.columns],
                                    data=df.to_dict('records'),
                                    style_data={
                                        'whiteSpace': 'normal',
                                        'height': 'auto',
                                        'lineHeight': '15px'
                                    },
                                    style_cell={'textAlign': 'left',
                                                'backgroundColor': 'rgb(224, 224, 224)',
                                                'color': 'black'},
                                    fixed_rows={'headers': True},
                                    page_action='none',     # render all of the data at once
                                    style_table={
                                        'height': '700px', 'width': '1000px'},
                                    style_header={
                                        'backgroundColor': 'rgb(51, 102, 0)',
                                        'font': 'bold'}
                                    )
