

from matplotlib.pyplot import ylabel
import pandas as pd  # (version 0.24.2)
import dash  # (version 1.0.0)
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
import numpy as np

import plotly.express as px

# the readDB function does the SQL interaction
from AssetMappr.database.readDB import readDB


def survey_Planner_cb(app):
    @app.callback(
        # Output('pie-chart-survey-for-planner', 'figure'),
        Output('bar-chart-survey-for-planner', 'figure'),
        [Input('survey-planner-view', 'data')],
        # [Input('rating-score-planner-view', 'data')]
        # Retrieves the relevant community's data from the dcc.Store object
    )
    def showPie(survey):
        surveyMap = pd.read_json(survey, orient='split')
        barchart = px.bar(
            surveyMap, x=surveyMap['What is your current use of the areas around the aquatorium?'])
        barchart.update_layout(
            margin=dict(l=20, r=20, t=8, b=20),
        )
        # return piechart, barchart
        return barchart
