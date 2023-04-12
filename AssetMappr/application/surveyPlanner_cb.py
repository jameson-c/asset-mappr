

from matplotlib.pyplot import ylabel
import pandas as pd  # (version 0.24.2)
import dash  # (version 1.0.0)
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import numpy as np

import plotly.express as px

# the readDB function does the SQL interaction
from AssetMappr.database.readDB import readDB


def survey_Planner_cb(app):
    @app.callback(
        Output('pie-chart-survey-for-planner', 'figure'),
        Output('bar-chart-survey-for-planner', 'figure'),
        Output('response-number-survey-for-planner', 'children'),
        [Input('survey-planner-view', 'data')],
        # [Input('rating-score-planner-view', 'data')]
        # Retrieves the relevant community's data from the dcc.Store object
    )
    def showPie(survey):
        surveyMap = pd.read_json(survey, orient='split')
        # random_x = [100, 2000, 550]
        # names = ['A', 'B', 'C']
        question_lst = list(surveyMap.columns)
       
       #number of response
        number_of_response = len(surveyMap)
       
       #Q1
        barchart = px.bar(
            surveyMap, x=question_lst[0])
        
        barchart.update_layout(
            margin=dict(l=20, r=20, t=8, b=20),
        )
        #Q2
        q2= question_lst[1]
        q2_count = surveyMap.groupby(q2)[q2].count()
        piechart = px.pie(values=q2_count, names=pd.Series(q2_count.index))
        piechart.update_layout(
                    margin=dict(l=20, r=20, t=8, b=20),
                )
        return piechart, barchart, number_of_response
        # return barchart
