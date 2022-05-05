"""
File: suggest_missing_asset_db.py
Author: Mihir Bhaskar

Desc: Interacts with the database to write user-submitted missing asset suggestions to the missing assets table

TODOs:
    - Generalise community_geo_id
    - Standardise the database connection so I don't keep starting new connections

Input:
    - (str) User's IP address
    - (str) Name of the user submitting the suggestion
    - (str) Role of the user in the community
    - (str) Name of the missing asset 
    - (str) category associated with that missing asset
    - (str) Desc: description of the missing asset
    - (tuple) click_lat_lng: desired latitude and longitude of the missing asset
    - (int) community_geo_id: geo_id of the relevant community
   
Output: 
    - None: this function only writes to the SQL database directly
    
"""
import psycopg2
import uuid
from datetime import datetime

def suggest_missing_asset_db(ip, user_name, user_role, name, categories, desc, click_lat_lng, community_geo_id):

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
    suggestion_id = str(uuid.uuid4()) 
    asset_name = name
    community_geo_id = community_geo_id
    primary_category = categories
    description = desc
    latitude = click_lat_lng[0]
    longitude = click_lat_lng[1]
    user_name = user_name
    user_role = user_role
    user_upload_ip = ip
    
    generated_timestamp = datetime.now()
    
    # Write the info into missing assets table
    # Refer to the createDBstructure.py script to see the variable types and DB structure
    cursor.execute('''INSERT INTO missing_assets (suggestion_id, missing_asset_name, primary_category, user_community, 
                               latitude, longitude, generated_timestamp, user_name, user_role, user_upload_ip)
                      VALUES ('{}','{}','{}', {},{},{},TIMESTAMP '{}', '{}', '{}', '{}');'''.format(suggestion_id, asset_name, 
                      primary_category,community_geo_id, latitude, longitude, generated_timestamp, user_name, 
                      user_role, user_upload_ip))
       
    
    
    conn.commit()
    conn.close()
    
    return None
