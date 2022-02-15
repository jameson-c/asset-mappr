"""
File: display_table_cb.py
Author: Mihir Bhaskar

Desc: This file creates the callback which fetches the database from the server
      and returns a Dash Data Table displaying it.
      
      This is linked to the display_table.py layout file, through the output id 'main-table'

Input: 
    db: The database object
    app: an initialized dash app
Output: 
    A callback that returns a Dash Data Table with the SQL data 
"""
import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import dcc
from dash import html
import pandas as pd

def display_table_cb(app, db):
    
    @app.callback(Output('main-table', 'children'),
              [Input('interval_pg', 'n_intervals')])
    def populate_datatable(n_intervals):
        df = pd.read_sql_table('assets_preloaded', con=db.engine)
    
        return dash_table.DataTable(id='main_table',
                                    columns=[{'name':str(x), 'id':str(x)} for x in df.columns],
                                    data = df.to_dict('records'),
                                    fixed_rows={'headers': True})
    

    

