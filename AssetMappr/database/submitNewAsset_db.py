"""
File: submitNewAsset_db.py
Author: Mihir Bhaskar

Desc: Interacts with the database to write user-submitted assets to the staging assets table

TODOs:
    - Generalise community_geo_id
    - Standardise the database connection so I don't keep starting new connections

Input:
    - (str) Staged asset ID (generated as a UUID 36 character)
    - (str) User's IP address
    - (str) Name of the user submitting the asset
    - (str) Role of the user in the community
    - (str) Name of the asset 
    - (list) Categories associated with that asset
    - (str) Desc: description of the asset
    - (str) Site: website associated with the asset
    - (tuple) click_lat_lng: latitude and longitude of the asset
    - (int) community_geo_id: geo_id of the relevant community
    - (str) Address: the geocoded address associated with the lat-long
   
Output: 
    - None: this function only writes to the SQL database directly
    
"""
import psycopg2
import uuid
from datetime import datetime
import os

def submitNewAsset_db(staged_asset_id, ip, user_name, user_role, name, categories, desc, site, click_lat_lng, community_geo_id, address):

    # Getting database connection URI from environment
    con_string = os.getenv('DB_URI')

    # Establish connection with database (details found in Heroku dashboard after login)
    conn = psycopg2.connect(con_string)

    # Create cursor object
    cursor = conn.cursor()
    
    # Process the info into a suitable format for the staging asset table
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
    address = address
    
    generated_timestamp = datetime.now()
    
    # Write the info into staged assets table
    # Refer to the createDBstructure.py script to see the variable types and DB structure
    cursor.execute('''INSERT INTO staged_assets (staged_asset_id, asset_name, asset_type, community_geo_id, source_type, 
                               description, website, latitude, longitude, generated_timestamp, user_name, user_role, user_upload_ip, address)
                      VALUES ('{}','{}','{}',{},'{}','{}','{}',{},{},TIMESTAMP '{}', '{}', '{}', '{}', '{}');'''.format(staged_asset_id, asset_name, asset_type, community_geo_id, source_type, 
                               description, website, latitude, longitude, generated_timestamp, user_name, user_role, user_upload_ip, address))
       
    # Write information to the asset-categories table
    for cat in categories:
        cursor.execute('''INSERT INTO staged_asset_categories (staged_asset_id, category)
                           VALUES ('{}', '{}');'''.format(staged_asset_id, cat))    
    
    
    conn.commit()
    conn.close()
    
    return None
