"""
File: readDB.py
Author: Mihir Bhaskar

Desc: This file interacts with the postgreSQL database to read in the initial datasets when we initialise the app session

It has two functions; one which reads the master tables (not dependent on the community the user selects),
and one that reads in the community-specific datasets (assets, asset_categories for now)

TODO:
    -
    
Inputs:
    - app: an initialized Dash app
    - community_geo_id (pending implementation)
   
Outputs: (see the database documentation for more info on these tables)
    - df: data frame of the main assets table
    - asset_categories: data frame of the asset-categories table
    - master_categories: a list of the unique master category values
    - master_value_tags: a list of the unique master value tags (for use in the ratings function)

"""
import dash
import pandas as pd
from flask_sqlalchemy import SQLAlchemy

def readMasters():
    # con_string = 'postgresql://assetmappr_database_user:5uhs74LFYP5G2rsk6EGzPAptaStOb9T8@dpg-c9rifejru51klv494hag-a/assetmappr_database'
    
    # If running the app externally (e.g. outside render/locally), use this connection string instead:
    con_string = 'postgresql://assetmappr_database_user:5uhs74LFYP5G2rsk6EGzPAptaStOb9T8@dpg-c9rifejru51klv494hag-a.ohio-postgres.render.com/assetmappr_database'

    # Load the categories master list
    master_categories = pd.read_sql_table('categories_master', con=con_string)
    master_categories = master_categories.values.tolist()
    master_categories = [item for sublist in master_categories for item in sublist]
    
    # Load the values master list 
    master_value_tags = pd.read_sql_table('values_master', con=con_string)
    master_value_tags = master_value_tags.values.tolist()
    master_value_tags = [item for sublist in master_value_tags for item in sublist]
           
    # Load the communities master list
    master_communities = pd.read_sql_table('communities_master', con=con_string)

    return master_categories, master_value_tags, master_communities

def readDB(community_geo_id):
    
    # con_string = 'postgresql://assetmappr_database_user:5uhs74LFYP5G2rsk6EGzPAptaStOb9T8@dpg-c9rifejru51klv494hag-a/assetmappr_database'
    
    # If running the app externally (e.g. outside render/locally), use this connection string instead:
    con_string = 'postgresql://assetmappr_database_user:5uhs74LFYP5G2rsk6EGzPAptaStOb9T8@dpg-c9rifejru51klv494hag-a.ohio-postgres.render.com/assetmappr_database'
    
    # Load the main assets database    
    query = '''SELECT * FROM assets 
               WHERE community_geo_id = {}'''.format(community_geo_id)
    
    df = pd.read_sql(query, con=con_string)
    
    # Load the asset-categories mapping database for the relevant asset IDs
    query = '''SELECT * FROM asset_categories 
               WHERE asset_id IN
                   (SELECT asset_id FROM assets 
                    WHERE community_geo_id = {})
               '''.format(community_geo_id)
    
    asset_categories = pd.read_sql(query, con=con_string)
    
    # This column demarcates between assets read in from the DB and staged assets added by the user
    # in the current session, so they can be displayed on the map in different colors and ratings for
    # verified vs. staged assets can be distinguished
    df['asset_status'] = 'Verified'
    
    return df, asset_categories
