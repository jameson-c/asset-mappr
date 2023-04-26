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
import dash


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
        df_survey = df_survey[:-3]
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
        [Input('button_survey_csv', 'n_clicks')],
        [Input('choose-the-survey-source', 'value')],
        # Retrieves the relevant community's data from the dcc.Store object
        [Input('survey-planner-view', 'data')],
        prevent_initial_call=True,
    )
    def download_function_csv(csv_clicks, survey_name, survey_data):

        df_survey = pd.read_json(survey_data, orient='split')
        df_survey = df_survey[:-3]
        df_placeholder = pd.DataFrame(columns=['Question 1', 'Question 2', 'Question 3', 'Question 4', 'Question 5'],
                                      index=range(1, 10))

        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

        # Only if the button is clicked, initiate the download
        if 'button_survey_csv' in changed_id:
            if survey_name == 'Aquatorium Survey':
                # csv_button = 0
                return dcc.send_data_frame(df_survey.to_excel, "aquatorium survey.xlsx", sheet_name='aquatorium survey')
            if survey_name == 'Placeholder Survey':
                # csv_button = 0
                return dcc.send_data_frame(df_placeholder.to_excel, "placeholder.xlsx", sheet_name='placeholder')
            raise PreventUpdate
        # if survey_name == 'Aquatorium Survey':
        #     if n_clicks is not None and n_clicks > 0:
        #         return dcc.send_data_frame(df_survey.to_excel, "aquatorium survey.xlsx", sheet_name='aquatorium survey')
        # if survey_name == 'Placeholder Survey':
        #     if n_clicks is not None and n_clicks > 0:
        #         return dcc.send_data_frame(df_placeholder.to_excel, "placeholder.xlsx", sheet_name='placeholder')

    @app.callback(
        Output('download-survey-pdf', 'data'),
        [Input('button_survey_pdf', 'n_clicks')],
        [Input('choose-the-survey-source', 'value')],
        # Retrieves the relevant community's data from the dcc.Store object
        [Input('survey-planner-view', 'data')],
        prevent_initial_call=True,
    )
    def download_function_pdf(pdf_button, survey_name, survey_data):
        df_survey = pd.read_json(survey_data, orient='split')
        df_placeholder = pd.DataFrame(columns=['Question 1', 'Question 2', 'Question 3', 'Question 4', 'Question 5'],
                                      index=range(1, 10))
        # generating survey figure for survey pdf
        survey_figure = go.Figure(data=[go.Table(
            header=dict(values=list(df_survey.columns),
                        fill_color='paleturquoise',
                        font_size=8,
                        align='left'),
            cells=dict(values=[df_survey['What is your current use of the areas around the aquatorium?'],
                               df_survey['What makes this particular asset valuable for you?'],
                               df_survey['What do we have there now that can be improved?'],
                               df_survey['What are some obstacles/barriers to using the aquatorium as an event space?'],
                               df_survey['Do you have or see any accessibility issues that stop you from using the aquatorium?'],
                               df_survey['What would encourage you to make better use of the aquatorium and surrounding areas?'],
                               df_survey['How would you rate the safety of the aquatorium area?'],
                               df_survey['What are some of the ways we can improve safety?'],
                               df_survey['How would you rate the importance of the aquatorium for the local community?']],
                       fill_color='lavender',
                       font_size=8,
                       align='left'))
        ])
        survey_figure.update_layout(width=1100, height=800)

        # generating placeholder figure for survey pdf
        placeholder_figure = go.Figure(data=[go.Table(
            header=dict(values=list(df_placeholder.columns),
                        font_size=8,
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[df_placeholder['Question 1'],
                               df_placeholder['Question 2'],
                               df_placeholder['Question 3'],
                               df_placeholder['Question 4'],
                               df_placeholder['Question 5']],
                       fill_color='lavender',
                       font_size=8,
                       align='left'))
        ])
        placeholder_figure.update_layout(width=1100, height=800)

        fmt = "pdf"
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        # Only if the button is clicked, initiate the download

# @app.callback(Output(component_id='my-div', component_property='children'),
#     [Input('btn-nclicks-1', 'n_clicks'), Input('adding-rows-table', 'data')])
# def update_output_div(n_clicks, data):

#     changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

#     if 'btn-nclicks-1' in changed_id:

#         print(data)
#         # n_clicks = 0
#         # return n_clicks

#     else:

#         print("else loop")

        if 'button_survey_pdf' in changed_id:
            if survey_name == 'Aquatorium Survey':
                print('test: the survey name aqua', pdf_button)
                return dcc.send_bytes(lambda x: write_image(survey_figure, x, format=fmt), "aquatorium survey.{}".format(fmt))
            if survey_name == 'Placeholder Survey':
                print('test: the survey name placeholder', pdf_button)
                return dcc.send_bytes(lambda x: write_image(placeholder_figure, x, format=fmt), "placeholder survey.{}".format(fmt))
            raise PreventUpdate
