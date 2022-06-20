from itertools import count
import pandas as pd  # (version 0.24.2)
import datetime as dt
import dash  # (version 1.0.0)
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly  # (version 4.4.1)
import plotly.express as px


def showStatCat_cb(app, asset_categories):
    dff = asset_categories.groupby('category').count()

    @app.callback(
        Output(component_id='bar-chart-for-planner',
               component_property='figure'),
        Input('choose-the-stat', 'value'))
    def showChart(count_number):

        barchart = px.bar(
            data_frame=dff,
            x=dff['asset_id'],
            # color="INDEX_NAME",
            opacity=0.9,
            barmode='group',
            orientation='h')
        barchart.update_layout(yaxis={'categoryorder': 'total ascending'})

        return barchart
