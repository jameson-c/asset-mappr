"""
File: submit_new_asset_db.py
Author: Mihir Bhaskar

Desc: Writes new asset to the staging assets database

TODOs:
    - Return back a 'row' that can be appended onto the dataframe 
    - Generalise community_geo_id
    - Standardise the database connection so I don't keep starting new connections

Input:
   
Output: 
    
"""
import psycopg2
import uuid
from datetime import datetime

def submit_new_asset_db(ip, user_name, user_role, name, categories, desc, site, click_lat_lng, community_geo_id):

    # Establish connection with database (details found in Heroku dashboard after login)
    conn = psycopg2.connect(
        database = 'dmt6i1v8bv5l1',
        user = 'ilohghqbmiloiv',
        password = 'f4fbd28e91d021bada72701576d41107b78bc515ad0b1e94d934939fbce7b2e6',
        host = 'ec2-54-235-98-1.compute-1.amazonaws.com',
        port = '5432'
        )

    # Create cursor object
    cursor = conn.cursor()
    
    # Process the info into a suitable format for the staging asset table
    staged_asset_id = str(uuid.uuid4())
    asset_name = name
    asset_type = 'Tangible'
    community_geo_id = community_geo_id
    source_type = 'User'
    description = desc
    website = site
    latitude = click_lat_lng[0]
    longitude = click_lat_lng[1]
    user_name = user_name
    user_role = user_role
    user_upload_ip = ip
    
    generated_timestamp = datetime.now()
    
    # Write the info into staged assets table
    cursor.execute('''INSERT INTO staged_assets (staged_asset_id, asset_name, asset_type, community_geo_id, source_type, 
                               description, website, latitude, longitude, generated_timestamp, user_name, user_role, user_upload_ip)
                      VALUES ('{}','{}','{}',{},'{}','{}','{}',{},{},TIMESTAMP '{}', '{}', '{}', '{}');'''.format(staged_asset_id, asset_name, asset_type, community_geo_id, source_type, 
                               description, website, latitude, longitude, generated_timestamp, user_name, user_role, user_upload_ip))
       
    # Write information to the asset-categories table
    for cat in categories:
        cursor.execute('''INSERT INTO staged_asset_categories (staged_asset_id, category)
                           VALUES ('{}', '{}');'''.format(staged_asset_id, cat))    
    
    
    conn.commit()
    conn.close()
    
    return None
