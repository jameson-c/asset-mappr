"""
File: readDB.py
Author: Mihir Bhaskar

Desc: This file interacts with the postgreSQL database to read in the initial datasets when we initialise the app session
Input: TODO: make the sql params an input into this

Other TODOs:
    - Make the input dependent on the community geo id
   

Output: 
    - A function that returns th
"""
import dash
import pandas as pd
from flask_sqlalchemy import SQLAlchemy


def readDB(community_geo_id=False):
    
    # Connect to the Heroku postgreSQL database
    server.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ilohghqbmiloiv:f4fbd28e91d021bada72701576d41107b78bc515ad0b1e94d934939fbce7b2e6@ec2-54-235-98-1.compute-1.amazonaws.com:5432/dmt6i1v8bv5l1'
    server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(server)
    
    # Load the categories master list
    master_categories = pd.read_sql_table('categories_master', con=db.engine)
    master_categories = master_categories.values.tolist()
    master_categories = [item for sublist in master_categories for item in sublist]
    
    # Load the values master list 
    master_value_tags = pd.read_sql_table('values_master', con=db.engine)
    master_value_tags = master_value_tags.values.tolist()
    master_value_tags = [item for sublist in master_value_tags for item in sublist]
    
    # Load the main assets database
    df = pd.read_sql_table('assets', con=db.engine)

    # Load the asset-categories mapping database
    asset_categories = pd.read_sql_table('asset_categories', con=db.engine)
    
    return df, asset_categories, master_categories, master_value_tags