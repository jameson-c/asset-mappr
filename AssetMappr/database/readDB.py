"""
File: readDB.py
Author: Mihir Bhaskar, Anna Wang

Desc: This file interacts with the postgreSQL database to read in the initial datasets when we initialise the app session
    
TODOs:
    - Connect to SQL centrally once, instead of starting many different connections
    - Make the input dependent on community_geo_id
    
Inputs:
    - app: an initialized Dash app
    - community_geo_id (pending implementation)
   
Outputs: (see the database documentation for more info on these tables)
    - df: data frame of the main assets table
    - asset_categories: data frame of the asset-categories table
    - master_categories: a list of the unique master category values
    - master_value_tags: a list of the unique master value tags (for use in the ratings function)
    - missing_assets: data frame of missing_assets table
    - rating_score: data frame of staged_rating tables
    - tagList_pos/neg: the positive and negative value list

"""
import pandas as pd
from flask_sqlalchemy import SQLAlchemy


def readMasters():

    # con_string = 'postgresql://assetmappr_database_user:5uhs74LFYP5G2rsk6EGzPAptaStOb9T8@dpg-c9rifejru51klv494hag-a/assetmappr_database'

    # If running the app externally (e.g. outside render/locally), use this connection string instead:
    con_string = 'postgresql://assetmappr_database_user:5uhs74LFYP5G2rsk6EGzPAptaStOb9T8@dpg-c9rifejru51klv494hag-a.ohio-postgres.render.com/assetmappr_database'

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
        - df: a data frame with the main assets table
        - asset_categories: a data frame mapping the assets in df to the categories they belong to

    '''

    # con_string = 'postgresql://assetmappr_database_user:5uhs74LFYP5G2rsk6EGzPAptaStOb9T8@dpg-c9rifejru51klv494hag-a/assetmappr_database'

    # If running the app externally (e.g. outside render/locally), use this connection string instead:
    con_string = 'postgresql://assetmappr_database_user:5uhs74LFYP5G2rsk6EGzPAptaStOb9T8@dpg-c9rifejru51klv494hag-a.ohio-postgres.render.com/assetmappr_database'

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

    # This column demarcates between assets read in from the DB and staged assets added by the user
    # in the current session, so they can be displayed on the map in different colors and ratings for
    # verified vs. staged assets can be distinguished
    # df['asset_status'] = 'Verified'
    return df_cnm, asset_categories, missing_assets, rating_score, rating_value
