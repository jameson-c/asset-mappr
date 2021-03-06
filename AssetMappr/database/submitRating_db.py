"""
File: submitRating_db.py
Author: Anna Wang, Mihir Bhaskar

Desc: Interacts with the database to write ratings to the staged ratings table and staged value tables;


Input:
    - (str) ip: the IP address from which the user is uploading the rating
    - (str) asset_id: the asset ID to which the rating pertains 
    - (int) rating_score: score selected on scale of 0-5
    - (str) rating_comments: text string with any comments the user gave in the review
    - (int) community_geo_id: the relevant community geo ID
    - (str) value: value tags which the user choose for the asset
   
Output: 
    - None: this function only writes to the SQL database directly
    
"""
import psycopg2
import uuid
from datetime import datetime
import os

def submitRating_db(ip, asset_id, rating_score, rating_comments, community_geo_id, value_tag):
    
    # Getting database connection URI from environment
    con_string = os.getenv('DB_URI')

    # Establish connection with database (details found in Heroku dashboard after login)
    conn = psycopg2.connect(con_string)

    # Create cursor object
    cursor = conn.cursor()

    # Create a UID for the rating
    staged_rating_id = str(uuid.uuid4())
    
    user_upload_ip = ip
    
    rating_scale = rating_score
    comments = rating_comments
    user_community = community_geo_id 

    generated_timestamp = datetime.now()

    value = value_tag

    # Write info into staged ratings table
    cursor.execute('''INSERT INTO staged_ratings (user_upload_ip, staged_rating_id, asset_id, user_community, generated_timestamp,
                   rating_scale, comments)
                 VALUES ('{}','{}', '{}', {}, TIMESTAMP '{}', {}, '{}');'''.format(user_upload_ip, staged_rating_id, asset_id, user_community,
                 generated_timestamp, rating_scale, comments))
    
    # Write info into staged value table
    for val in value:
        cursor.execute('''INSERT INTO staged_values (staged_rating_id, value)
                VALUES ('{}', '{}');'''.format(staged_rating_id, val))

    conn.commit()
    conn.close()

    return None
