

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
        Output('bar-chart-q3-survey-for-planner', 'figure'),
        Output('response-number-survey-for-planner', 'children'),
        Output('q1-survey-for-planner', 'children'),
        Output('q2-survey-for-planner', 'children'),
        Output('q3-survey-for-planner', 'children'),
        [Input('survey-planner-view', 'data')],
        # Retrieves the relevant community's data from the dcc.Store object
    )
    def showPie(survey):
        surveyMap = pd.read_json(survey, orient='split')
        question_lst = list(surveyMap.columns)

       # number of response
        number_of_response = len(surveyMap)

       # Q1
        q1 = question_lst[0]
        barchart = px.bar(
            surveyMap, x=q1)

        barchart.update_layout(
            margin=dict(l=20, r=20, t=8, b=20),
            xaxis={'title': ' '},
            yaxis={'title': 'Number of People'}
        )

        barchart.update_yaxes(tick0=0, dtick=1)

        # Q2
        q2 = question_lst[1]
        q2_count = surveyMap.groupby(q2)[q2].count()
        piechart = px.pie(values=q2_count, names=pd.Series(q2_count.index))
        piechart.update_layout(
            # margin=dict(l=20, r=20, t=8, b=20),
            showlegend=False
            # legend=dict(x=0.4, y=1.2),
        )

        # q3
        q3 = question_lst[2]
        barchart_q3 = px.bar(
            surveyMap, y=q3, orientation='h')

        barchart_q3.update_layout(
            margin=dict(l=20, r=20, t=8, b=20),
            xaxis={'title': 'Number of People'},
            yaxis={'title': ' '}
        )

        barchart_q3.update_yaxes(tick0=0, dtick=1)

        return piechart, barchart, barchart_q3, number_of_response, q1, q2, q3


# from matplotlib.pyplot import ylabel
# import pandas as pd  # (version 0.24.2)
# import dash  # (version 1.0.0)
# from dash import dcc
# import dash_bootstrap_components as dbc
# from dash import html
# from dash.dependencies import Input, Output
# import numpy as np

# import plotly.express as px

# # the readDB function does the SQL interaction
# from AssetMappr.database.readDB import readDB


# def survey_Planner_cb(app):
#     @app.callback(
#         # Output('pie-chart-survey-for-planner', 'figure'),
#         Output('bar-chart-survey-for-planner', 'figure'),
#         [Input('survey-planner-view', 'data')],
#         # [Input('rating-score-planner-view', 'data')]
#         # Retrieves the relevant community's data from the dcc.Store object
#     )
#     def showPie(survey):
#         surveyMap = pd.read_json(survey, orient='split')
#         barchart = px.bar(
#             surveyMap, x=surveyMap['What is your current use of the areas around the aquatorium?'])
#         barchart.update_layout(
#             margin=dict(l=20, r=20, t=8, b=20),
#         )
#         # return piechart, barchart
#         return barchart
