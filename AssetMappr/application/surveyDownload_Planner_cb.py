"""
File: surveyDownload_Planner_cb.py
Author: Olivia Hao
Desc: This file creates the callbacks that generate the survey display and download option in the planner view

This is linked to the surveyDownload_Planner.py feature in presentation

Input:
    app: an initialized dash app
    df: main data frame with assets to be displayed
    survey: data frame with survey questions and responses

Output:
    Callbacks relating to the showMap_Planner feature

"""
from dash.dependencies import Input, Output, State
from dash import html, dcc
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.io import write_image
from dash import dash_table
from collections import OrderedDict
import xlsxwriter
from dash.exceptions import PreventUpdate


def surveyDownload_Planner_cb(app):

    # This callback receives input on which type of assets the user has selected
    # And outputs the table object

    @app.callback(Output('survey-table', 'children'),
                  [Input('choose-the-survey-source', 'value')],
                  [Input('survey-planner-view', 'data')]
                  )
    def update_table(survey_name, survey_data):

        # Transform the JSON format data from the dcc.Store back into data frames
        df_survey = pd.read_json(survey_data, orient='split')
        df_placeholder = pd.DataFrame(columns=['Question 1', 'Question 2', 'Question 3', 'Question 4', 'Question 5'],
                                      index=range(1, 10))

        if survey_name == 'Aquatorium Survey':
            # Data needs to be converted into a dictionary format to be read by dash Data Table
            tmpdta = df_survey.to_dict('rows')
            data_columns = ['What is your current use of the areas around the aquatorium?',
                            'What makes this particular asset valuable for you?',
                            'What do we have there now that can be improved?',
                            'What are some obstacles/barriers to using the aquatorium as an event space?',
                            'Do you have or see any accessibility issues that stop you from using the aquatorium?',
                            'What would encourage you to make better use of the aquatorium and surrounding areas?',
                            'How would you rate the safety of the aquatorium area?',
                            'What are some of the ways we can improve safety?',]
            df_columns = ['What is your current use of the areas around the aquatorium?',
                          'What makes this particular asset valuable for you?',
                          'What do we have there now that can be improved?',
                          'What are some obstacles/barriers to using the aquatorium as an event space?',
                          'Do you have or see any accessibility issues that stop you from using the aquatorium?',
                          'What would encourage you to make better use of the aquatorium and surrounding areas?',
                          'How would you rate the safety of the aquatorium area?',
                          'What are some of the ways we can improve safety?',]

        # Case when type = Placeholder Survey
        if survey_name == 'Placeholder Survey':
            # Data needs to be converted into a dictionary format to be read by dash Data Table
            tmpdta = df_placeholder.to_dict('rows')
            data_columns = ['Question 1', 'Question 2',
                            'Question 3', 'Question 4', 'Question 5']
            df_columns = ['Question 1', 'Question 2',
                          'Question 3', 'Question 4', 'Question 5']
        # Return a Dash Data Table with the relevant data
        return dash_table.DataTable(data=tmpdta, columns=[{'name': col, 'id': df_columns[idx]} for (idx, col) in enumerate(data_columns)],
                                    filter_action='native',
                                    style_data_conditional=[{
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(220, 220, 220)'
                                    }],
                                    style_data={
                                        'whiteSpace': 'normal',
                                        'height': 'auto',
                                        'lineHeight': '15px',
                                        'minWidth': '180px', 'width': '200px', 'maxWidth': '220px',
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis',
        },

            style_header={
                                        'backgroundColor': 'white',
                                        'whiteSpace': 'normal',
                                        'height': 'auto',
                                        'lineHeight': '20px',
                                        'color': 'darkolivegreen',
                                        'fontSize': 14,
                                        'textAlign': 'center'

        },
            style_cell={'textAlign': 'left', 'fontSize': 13,
                        'font-family': 'sans-serif'},
            fixed_rows={'headers': True, 'data': 0})
        # test: return html.H1('Placeholder')

    # This callback interacts with the download button to download the table data as an Excel file
    @app.callback(
        Output('download-survey-xlsx', 'data'),
        [Input('choose-the-survey-source', 'value')],
        [Input('button_survey_csv', 'n_clicks')],
        # Retrieves the relevant community's data from the dcc.Store object
        [Input('survey-planner-view', 'data')],
        prevent_initial_call=True,
    )
    def download_function_csv(survey_name, csv_button, survey_data):
        df_survey = pd.read_json(survey_data, orient='split')
        df_placeholder = pd.DataFrame(columns=['Question 1', 'Question 2', 'Question 3', 'Question 4', 'Question 5'],
                                      index=range(1, 10))

        # Only if the button is clicked, initiate the download
        if csv_button:
            if survey_name == 'Aquatorium Survey':
                return dcc.send_data_frame(df_survey.to_excel, "aquatorium survey.xlsx", sheet_name='aquatorium survey')
            else:
                return dcc.send_data_frame(df_placeholder.to_excel, "placeholder.xlsx", sheet_name='placeholder')
            raise PreventUpdate

    @app.callback(
        Output('download-survey-pdf', 'data'),
        [Input('choose-the-survey-source', 'value')],
        [Input('button_survey_pdf', 'n_clicks')],
        # Retrieves the relevant community's data from the dcc.Store object
        [Input('survey-planner-view', 'data')],
        prevent_initial_call=True,
    )
    def download_function_pdf(survey_name, pdf_button, survey_data):
        df_survey = pd.read_json(survey_data, orient='split')
        df_placeholder = pd.DataFrame(columns=['Question 1', 'Question 2', 'Question 3', 'Question 4', 'Question 5'],
                                      index=range(1, 10))
        # generating survey figure for survey pdf
        survey_figure = go.Figure(data=[go.Table(
            header=dict(values=list(df_survey.columns),
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[df_survey.transpose().values.tolist()],
                       fill_color='lavender',
                       align='left'))
        ])

        # generating placeholder figure for survey pdf
        placeholder_figure = go.Figure(data=[go.Table(
            header=dict(values=list(df_placeholder.columns),
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[df_placeholder.transpose().values.tolist()],
                       fill_color='lavender',
                       align='left'))
        ])
        fmt = "pdf"
        # Only if the button is clicked, initiate the download
        if pdf_button:
            if survey_name == 'Aquatorium Survey':
                return dcc.send_bytes(lambda x: write_image(survey_figure, x, format=fmt), "aquatorium survey.{}".format(fmt))
            else:
                return dcc.send_bytes(lambda x: write_image(placeholder_figure, x, format=fmt), "placeholder survey.{}".format(fmt))
            raise PreventUpdate
