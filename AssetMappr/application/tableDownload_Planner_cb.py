
"""
File: tableDownload_Planner_cb.py
Author: Mihir Bhaskar, Anna Wang
Desc: This file creates the callbacks that generate the table display and download option in the planner view
      
This is linked to the tableDownload_Planner.py feature in presentation
Input: 
    app: an initialized dash app
    df: main data frame with assets to be displayed
    asset_categories: data frame with assets and their catagories (in separate df because 1 asset can have many cats)
    missing_assets: data frame with suggestion assets from community members
    rating_score: data frame of the ratings table
    rating_values: data frame of the rating-value tag mapping for each rating
Output: 
    Callbacks relating to the showMap_Planner feature
     
"""
from dash.dependencies import Input, Output, State
from dash import html, dcc
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.io import write_image
from dash.exceptions import PreventUpdate


from dash import dash_table
from collections import OrderedDict
import xlsxwriter


def tableDownload_Planner_cb(app):

    # This callback receives input on which type of assets the user has selected
    # And outputs the table object

    @app.callback(Output('data-table', 'children'),
                  [Input('choose-the-table-source', 'value')],
                  # Retrieves the relevant community's data from the dcc.Store object
                  [Input('assets-df', 'data')],
                  [Input('asset-categories-cnm', 'data')],
                  [Input('missing-assets-planner-view', 'data')],
                  [Input('rating-score-planner-view', 'data')],
                  [Input('rating-value-planner-view', 'data')],
                  )
    def update_table(type_of_assets, df_cnm, asset_categories, missing_assets, rating_score, rating_values):

        # Transform the JSON format data from the dcc.Store back into data frames
        df_cnm = pd.read_json(df_cnm, orient='split')
        asset_categories = pd.read_json(asset_categories, orient='split')
        missing_assets = pd.read_json(missing_assets, orient='split')
        rating_score = pd.read_json(rating_score, orient='split')
        rating_values = pd.read_json(rating_values, orient='split')

        ### MAKING THE EXISTING ASSETS TABLE - PULLING TOGETHER ALL USEFUL INFO ###

        # Keeping relevant columns in the main assets
        df = df_cnm[['asset_id', 'asset_name',
                     'description', 'address', 'website']]

        ## MERGING ON CATEGORY INFO ##

        # Making asset_categories data wide (asset_id, category_1, category_2, etc.) so it can be merged uniquely
        # with df, and displayed in one row alongside the other asset information

        # Starting a counter variable in asset categories within each asset ID
        asset_categories['counter'] = asset_categories.groupby(
            'asset_id').cumcount() + 1

        # Converting to string so now the counter variable = 'category_1' for an asset's first category, 'category_2'
        # for an asset's second category, etc.
        asset_categories['counter'] = asset_categories['counter'].apply(str)
        asset_categories['counter'] = 'category_' + asset_categories['counter']

        # Pivoting to wide
        asset_categories = asset_categories.pivot(
            index='asset_id', columns='counter', values='category')

        # Merging the category info
        df = pd.merge(df, asset_categories, on='asset_id')

        ## MERGING ON RATINGS INFO ##

        # Add asset_id to rating values table
        rating_values = pd.merge(rating_values, rating_score[[
            'staged_rating_id', 'asset_id']], on='staged_rating_id')

        # Merge the rating values table with the
        asset_values = pd.merge(df, rating_values, on='asset_id')

        # Aggregate this table by asset_id to get the most common rated tag for each asset
        asset_values = asset_values.groupby('asset_id').agg(
            most_common_rated_value=('value', lambda x: x.value_counts().index[0]))

        # pull asset_id out of the index for later use in merging
        asset_values = asset_values.reset_index()

        # Merge the most common rated value info
        df = pd.merge(df, asset_values, on='asset_id', how='left')

        # Collapse ratings table down to one observation per asset, which is the average rating score and number of ratings
        avg_rating_assets = rating_score.groupby('asset_id').agg(avg_asset_rating=('rating_scale', np.mean),
                                                                 num_ratings=('staged_rating_id', np.count_nonzero))
        # pull asset_id out of index fo rlater use in merging
        avg_rating_assets = avg_rating_assets.reset_index()

        # Merging this info on
        df = pd.merge(df, avg_rating_assets, on='asset_id', how='left')

        # Processing the comments

        comments_df = rating_score[['asset_id', 'comments']]
        comments_df = comments_df.dropna(subset=['comments'])
        comments_df = comments_df[~comments_df['comments'].isin(['', ' '])]

        # Join all the comments together into a single string, in a comlumn called 'all_comments'
        # Each unique comment is separated by " | "
        comments_df['all_comments'] = comments_df.groupby(
            'asset_id')['comments'].transform(lambda x: ' | '.join(x))
        comments_df = comments_df.drop_duplicates('asset_id')

        # Merge this onto the overall df
        df = pd.merge(
            df, comments_df[['asset_id', 'all_comments']], on='asset_id', how='left')

        df['avg_asset_rating'] = round(df['avg_asset_rating'], 2)

        ### MAKING THE MISSING ASSETS TABLE ###

        # Keeping relevant columns
        missing_df = missing_assets[['missing_asset_name', 'description',
                                    'primary_category', 'address', 'justification', 'generated_timestamp']]

        if type_of_assets == 'Existing Assets':
            # Data needs to be converted into a dictionary format to be read by dash Data Table
            tmpdta = df.to_dict('rows')
            data_columns = ['Asset Name', 'Description', 'Address', 'Website', 'Category1', 'Category2',
                            'Popular Value Tag', 'Average Rating Score', 'Number of Ratings', 'Comments']
            df_columns = ['asset_name', 'description', 'address', 'website', 'category_1', 'category_2',
                          'most_common_rated_value', 'avg_asset_rating', 'num_ratings', 'all_comments']

        # Case when type = Missing Assets
        else:
            # Data needs to be converted into a dictionary format to be read by dash Data Table
            tmpdta = missing_df.to_dict('rows')
            data_columns = ['Asset Name', 'Description',
                            'Primary Category', 'Address', 'Justification', 'Time']
            df_columns = ['missing_asset_name', 'description', 'primary_category',
                          'address', 'justification', 'generated_timestamp']
        # Return a Dash Data Table with the relevant data
        return dash_table.DataTable(data=tmpdta, columns=[{'name': col, 'id': df_columns[idx]} for (idx, col) in enumerate(data_columns)],
                                    filter_action='native',
                                    style_data_conditional=[{
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(220, 220, 220)'
                                    }],
                                    style_data={
                                        'whiteSpace': 'normal',
                                        'height': '25px',
                                        'lineHeight': '15px',
                                        'minWidth': '100px', 'width': '160px', 'maxWidth': '180px',
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis',
        },

            style_header={
                                        'backgroundColor': 'white',
                                        'color': 'darkolivegreen',
                                        'fontSize': 16,
                                        'textAlign': 'center'

        },
            style_cell={
                                        'textAlign': 'left', 'fontSize': 13, 'font-family': 'sans-serif'},
            fixed_rows={'headers': True, 'data': 0}),

    # This callback interacts with the download button to download the table data as an Excel file

    @app.callback(
        Output('download-dataframe-xlsx', 'data'),
        # Download only triggers when button is clicked, hence INput-State pair
        [Input('download_button_csv', 'n_clicks')],
        # Retrieves the relevant community's data from the dcc.Store object
        [Input('assets-df', 'data')],
        [Input('asset-categories-cnm', 'data')],
        [Input('missing-assets-planner-view', 'data')],
        [Input('rating-score-planner-view', 'data')],
        [Input('rating-value-planner-view', 'data')],
        [State('choose-the-table-source', 'value')],
        prevent_initial_call=True,
    )
    def download_function_csv(csv_clicks, df_cnm, asset_categories, missing_assets, rating_score, rating_values, type_of_assets):

        # Transform the JSON format data from the dcc.Store back into data frames
        df_cnm = pd.read_json(df_cnm, orient='split')
        asset_categories = pd.read_json(asset_categories, orient='split')
        missing_assets = pd.read_json(missing_assets, orient='split')
        rating_score = pd.read_json(rating_score, orient='split')
        rating_values = pd.read_json(rating_values, orient='split')

        ### MAKING THE EXISTING ASSETS TABLE - PULLING TOGETHER ALL USEFUL INFO ###

        # Keeping relevant columns in the main assets
        df = df_cnm[['asset_id', 'asset_name',
                     'description', 'address', 'website']]

        ## MERGING ON CATEGORY INFO ##

        # Making asset_categories data wide (asset_id, category_1, category_2, etc.) so it can be merged uniquely
        # with df, and displayed in one row alongside the other asset information

        # Starting a counter variable in asset categories within each asset ID
        asset_categories['counter'] = asset_categories.groupby(
            'asset_id').cumcount() + 1

        # Converting to string so now the counter variable = 'category_1' for an asset's first category, 'category_2'
        # for an asset's second category, etc.
        asset_categories['counter'] = asset_categories['counter'].apply(str)
        asset_categories['counter'] = 'category_' + asset_categories['counter']

        # Pivoting to wide
        asset_categories = asset_categories.pivot(
            index='asset_id', columns='counter', values='category')

        # Merging the category info
        df = pd.merge(df, asset_categories, on='asset_id')

        ## MERGING ON RATINGS INFO ##

        # Add asset_id to rating values table
        rating_values = pd.merge(rating_values, rating_score[[
            'staged_rating_id', 'asset_id']], on='staged_rating_id')

        # Merge the rating values table with the
        asset_values = pd.merge(df, rating_values, on='asset_id')

        # Aggregate this table by asset_id to get the most common rated tag for each asset
        asset_values = asset_values.groupby('asset_id').agg(
            most_common_rated_value=('value', lambda x: x.value_counts().index[0]))

        # pull asset_id out of the index for later use in merging
        asset_values = asset_values.reset_index()

        # Merge the most common rated value info
        df = pd.merge(df, asset_values, on='asset_id', how='left')

        # Collapse ratings table down to one observation per asset, which is the average rating score and number of ratings
        avg_rating_assets = rating_score.groupby('asset_id').agg(avg_asset_rating=('rating_scale', np.mean),
                                                                 num_ratings=('staged_rating_id', np.count_nonzero))
        # pull asset_id out of index fo rlater use in merging
        avg_rating_assets = avg_rating_assets.reset_index()

        # Merging this info on
        df = pd.merge(df, avg_rating_assets, on='asset_id', how='left')

        # Processing the comments

        comments_df = rating_score[['asset_id', 'comments']]
        comments_df = comments_df.dropna(subset=['comments'])
        comments_df = comments_df[~comments_df['comments'].isin(['', ' '])]

        # Join all the comments together into a single string, in a comlumn called 'all_comments'
        # Each unique comment is separated by " | "
        comments_df['all_comments'] = comments_df.groupby(
            'asset_id')['comments'].transform(lambda x: ' | '.join(x))
        comments_df = comments_df.drop_duplicates('asset_id')

        # Merge this onto the overall df
        df = pd.merge(
            df, comments_df[['asset_id', 'all_comments']], on='asset_id', how='left')

        df['avg_asset_rating'] = round(df['avg_asset_rating'], 2)

        ### MAKING THE MISSING ASSETS TABLE ###

        # Keeping relevant columns
        missing_df = missing_assets[['missing_asset_name', 'description',
                                    'primary_category', 'address', 'justification', 'generated_timestamp']]

        # Only if the button is clicked, initiate the download
        if csv_clicks:
            if type_of_assets == 'Existing Assets':
                return dcc.send_data_frame(df.to_excel, "existing_assets.xlsx", sheet_name='Existing Assets')
            if type_of_assets == 'Missing Assets':
                return dcc.send_data_frame(missing_df.to_excel, "missing_asset_suggestions.xlsx", sheet_name='Missing Suggested Assets')
            raise PreventUpdate

    @app.callback(
        Output('download-dataframe-pdf', 'data'),
        # Download only triggers when button is clicked, hence INput-State pair
        [Input('download_button_pdf', 'n_clicks')],
        # Retrieves the relevant community's data from the dcc.Store object
        [Input('assets-df', 'data')],
        [Input('asset-categories-cnm', 'data')],
        [Input('missing-assets-planner-view', 'data')],
        [Input('rating-score-planner-view', 'data')],
        [Input('rating-value-planner-view', 'data')],
        [State('choose-the-table-source', 'value')],
        prevent_initial_call=True,
    )
    def download_function_pdf(pdf_clicks, df_cnm, asset_categories, missing_assets, rating_score, rating_values, type_of_assets):

        # Transform the JSON format data from the dcc.Store back into data frames
        df_cnm = pd.read_json(df_cnm, orient='split')
        asset_categories = pd.read_json(asset_categories, orient='split')
        missing_assets = pd.read_json(missing_assets, orient='split')
        rating_score = pd.read_json(rating_score, orient='split')
        rating_values = pd.read_json(rating_values, orient='split')

        ### MAKING THE EXISTING ASSETS TABLE - PULLING TOGETHER ALL USEFUL INFO ###

        # Keeping relevant columns in the main assets
        df = df_cnm[['asset_id', 'asset_name',
                    'description', 'address', 'website']]

        ## MERGING ON CATEGORY INFO ##

        # Making asset_categories data wide (asset_id, category_1, category_2, etc.) so it can be merged uniquely
        # with df, and displayed in one row alongside the other asset information

        # Starting a counter variable in asset categories within each asset ID
        asset_categories['counter'] = asset_categories.groupby(
            'asset_id').cumcount() + 1

        # Converting to string so now the counter variable = 'category_1' for an asset's first category, 'category_2'
        # for an asset's second category, etc.
        asset_categories['counter'] = asset_categories['counter'].apply(str)
        asset_categories['counter'] = 'category_' + asset_categories['counter']

        # Pivoting to wide
        asset_categories = asset_categories.pivot(
            index='asset_id', columns='counter', values='category')

        # Merging the category info
        df = pd.merge(df, asset_categories, on='asset_id')

        ## MERGING ON RATINGS INFO ##

        # Add asset_id to rating values table
        rating_values = pd.merge(rating_values, rating_score[[
            'staged_rating_id', 'asset_id']], on='staged_rating_id')

        # Merge the rating values table with the
        asset_values = pd.merge(df, rating_values, on='asset_id')

        # Aggregate this table by asset_id to get the most common rated tag for each asset
        asset_values = asset_values.groupby('asset_id').agg(
            most_common_rated_value=('value', lambda x: x.value_counts().index[0]))

        # pull asset_id out of the index for later use in merging
        asset_values = asset_values.reset_index()

        # Merge the most common rated value info
        df = pd.merge(df, asset_values, on='asset_id', how='left')

        # Collapse ratings table down to one observation per asset, which is the average rating score and number of ratings
        avg_rating_assets = rating_score.groupby('asset_id').agg(avg_asset_rating=('rating_scale', np.mean),
                                                                 num_ratings=('staged_rating_id', np.count_nonzero))
        # pull asset_id out of index fo rlater use in merging
        avg_rating_assets = avg_rating_assets.reset_index()

        # Merging this info on
        df = pd.merge(df, avg_rating_assets, on='asset_id', how='left')

        # Processing the comments

        comments_df = rating_score[['asset_id', 'comments']]
        comments_df = comments_df.dropna(subset=['comments'])
        comments_df = comments_df[~comments_df['comments'].isin(['', ' '])]

        # Join all the comments together into a single string, in a comlumn called 'all_comments'
        # Each unique comment is separated by " | "
        comments_df['all_comments'] = comments_df.groupby(
            'asset_id')['comments'].transform(lambda x: ' | '.join(x))
        comments_df = comments_df.drop_duplicates('asset_id')

        # Merge this onto the overall df
        df = pd.merge(
            df, comments_df[['asset_id', 'all_comments']], on='asset_id', how='left')

        df['avg_asset_rating'] = round(df['avg_asset_rating'], 2)
        ### MAKING THE EXISTING ASSETS FIGURE ###
        # generating existing asset figure for pdf
        df_copy = df[['asset_name', 'description', 'address', 'website', 'category_1', 'category_2',
                      'most_common_rated_value', 'avg_asset_rating', 'num_ratings', 'all_comments']].copy()

        df_copy.columns = ['AssetName', 'Description', 'Address', 'Website', 'Category1', 'Category2',
                           'PopularValueTag', 'AverageRatingScore', 'NumberOfRatings', 'Comments']
        existing_figure = go.Figure(data=[go.Table(
            header=dict(values=list(df_copy.columns),
                        fill_color='paleturquoise',
                        font_size=8,
                        align='left'),
            cells=dict(values=[df_copy.AssetName, df_copy.Description, df_copy.Address, df_copy.Website,
                               df_copy.Category1, df_copy.Category2, df_copy.PopularValueTag, df_copy.AverageRatingScore,
                               df_copy.NumberOfRatings, df_copy.Comments],
                       fill_color='lavender',
                       font_size=8,
                       align='left'))
        ])
        existing_figure.update_layout(width=1200, height=6000)
        # Keeping relevant columns
        missing_df = missing_assets[['missing_asset_name', 'description',
                                    'primary_category', 'address', 'justification', 'generated_timestamp']]
        missing_df.columns = ['AssetName', 'Description',
                              'PrimaryCategory', 'Address', 'Justification', 'Time']
        # generating missing asset figure for pdf
        missing_figure = go.Figure(data=[go.Table(
            header=dict(values=list(missing_df.columns),
                        fill_color='paleturquoise',
                        font_size=8,

                        align='left'),
            cells=dict(values=[missing_df.AssetName, missing_df.Description,
                               missing_df.PrimaryCategory, missing_df.Address,
                               missing_df.Justification, missing_df.Time],
                       fill_color='lavender',
                       font_size=8,
                       align='left'))
        ])
        missing_figure.update_layout(width=1100, height=800)

        fmt = "pdf"

        # Only if the button is clicked, initiate the download
        if pdf_clicks:
            if type_of_assets == 'Existing Assets':
                print('test: existing', pdf_clicks)
                return dcc.send_bytes(lambda x: write_image(existing_figure, x, format=fmt), "existing asset.{}".format(fmt))
            if type_of_assets == 'Missing Assets':
                print('test: missing', pdf_clicks)
                return dcc.send_bytes(lambda x: write_image(missing_figure, x, format=fmt), "missing asset.{}".format(fmt))
            raise PreventUpdate
