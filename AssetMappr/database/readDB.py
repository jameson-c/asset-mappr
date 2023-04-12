"""
File: readDB.py
Author: Mihir Bhaskar, Anna Wang

Desc: This file interacts with the postgreSQL database to read in data we need for the app

It has two functions: readMasters(), which reads all the standard info that is independent of the selected community,
and readDB(), which reads the tables of information about assets and ratings relevant for the chosen community

See the database documentation here for more info about the DB structure and tables:
    https://docs.google.com/document/d/1lKTvWjOiNHWJKcMsqipY3JN79LT2jm9fHox5TMSI-ew/edit?usp=sharing
    
"""
import pandas as pd
from sqlalchemy import create_engine
import os
import json


def readMasters():
    '''
    Input: none
    Outputs:
        - master_categories: a list of the unique master category values
        - master_categories_desc: a list of the descriptions of what each category means
        - tagList_pos/neg: the positive and negative value list, from 'master values' associated with ratings
        - master_communities: a dataframe of all the communities incorporated into assetmappr
    '''
    # Loading the DB connection URI string from the environment
    con_string = os.getenv("DB_URI")

    # Load the categories master list
    master_category = pd.read_sql_table('categories_master', con=con_string)
    master_categories = master_category['category'].values.tolist()
    master_categories_desc = master_category['description'].values.tolist()

    # Load the values master list
    master_value_tags = pd.read_sql_table('values_master', con=con_string)
    tagList_pos = master_value_tags.loc[master_value_tags['value_type']
                                        == 'Positive', 'value'].tolist()
    tagList_neg = master_value_tags.loc[master_value_tags['value_type']
                                        == 'Negative', 'value'].tolist()
    master_value_tags = [i for i in master_value_tags['value']]

    # Load the communities master list
    master_communities = pd.read_sql_table(
        'communities_master', con=con_string)

    return master_categories, master_categories_desc, tagList_pos, tagList_neg, master_communities


def readDB(community_geo_id):
    '''
    Inputs: (int) community_geo_id: the geo ID of the selected community for which to retrieve info for from the DB
    Output:
        - df_cnm: a data frame with the main assets table for the chosen community
        - asset_categories: a data frame mapping the assets in df_cnm to the categories they belong to
        - missing_assets: data frame of missing_assets table for the community
        - rating_score: data frame of staged_rating tables
        - rating_value: data frame of the mapping of chosen value tags for each of the ratings 
    '''

    # Loading the DB connection URI string from the environment
    con_string = os.getenv('DB_URI')

    # Load the main assets database
    query = '''SELECT * FROM assets 
               WHERE community_geo_id = {}'''.format(community_geo_id)

    df_cnm = pd.read_sql(query, con=con_string)

    # Load the asset-categories mapping database for the relevant asset IDs
    query = '''SELECT * FROM asset_categories 
               WHERE asset_id IN
                   (SELECT asset_id FROM assets 
                    WHERE community_geo_id = {})
               '''.format(community_geo_id)

    asset_categories = pd.read_sql(query, con=con_string)

    # Load missing asstes
    query = '''SELECT * FROM missing_assets 
               WHERE user_community ={}'''.format(community_geo_id)

    missing_assets = pd.read_sql(query, con=con_string)

    # Load rating score
    query = '''SELECT * FROM staged_ratings 
               WHERE user_community ={}'''.format(community_geo_id)

    rating_score = pd.read_sql(query, con=con_string)

    # Load rating value
    query = '''SELECT * FROM staged_values 
               WHERE staged_rating_id IN
                   (SELECT staged_rating_id FROM staged_ratings 
                    WHERE user_community = {})
               '''.format(community_geo_id)

    rating_value = pd.read_sql(query, con=con_string)

    #load survey questions
    query = '''SELECT questions FROM survey_table'''
    survey_questions = pd.read_sql(query, con=con_string)

    out = survey_questions.to_json(orient='records')
    data = json.loads(out)
    q_value = []
    for i in data:
        q_dict = i['questions']
        temp = json.loads(q_dict)
        for j in range(1,9):
            q_value.append(temp[str(j)]['question'])

    #load survey response
    query = '''SELECT response FROM survey_response 
                WHERE survey_date >= '2023-03-24 00:00:00' '''
    survey_responses = pd.read_sql(query, con=con_string)

    out = survey_responses.to_json(orient='records')
    data = json.loads(out)
    response_values = []
    for i in data:
        response_dict = i["response"]
        response_value = []
        for j in range(1, 9):
            if str(j) in response_dict:
                temp = json.loads(response_dict[str(j)])
                response_value.append(temp['value'])
            else:
                response_value.append(None)
        response_values.append(response_value)

    data_dict = {}
    for col in range(len(q_value)):
        col_name = q_value[col]
        data_dict[col_name] = [lst[col] for lst in response_values]
    survey = pd.DataFrame(data_dict)
    print(survey)


    # This column demarcates between assets read in from the DB and staged assets added by the user
    # in the current session, so they can be displayed on the map in different colors and ratings for
    # verified vs. staged assets can be distinguished
    # df['asset_status'] = 'Verified'

    return df_cnm, asset_categories, missing_assets, rating_score, rating_value, survey