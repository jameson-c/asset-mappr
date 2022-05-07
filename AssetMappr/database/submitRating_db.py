"""
File: submitRating_db.py
Author: Anna Wang, Mihir Bhaskar

Desc: Interacts with the database to write ratings to the staged ratings table

TODOs:
    - Generalise community_geo_id
    - Standardise the database connection so I don't keep starting new connections

Input:
    - (str) asset_id: the asset ID to which the rating pertains 
    - (int) rating_score: score selected on scale of 0-5
    - (str) rating_comments: text string with any comments the user gave in the review
   
Output: 
    - None: this function only writes to the SQL database directly
    
"""
import psycopg2
import uuid
from datetime import datetime

def submitRating_db(asset_id, rating_score, rating_comments):
    
    # When deploying on Render, use this string
    con_string = 'postgresql://assetmappr_db_user:hyx8dhtgdq6mvyIfe3ANC2O7ceRheEr5@dpg-c9rao5j97ej5m8i836r0-a/assetmappr_db'
    
    # If running the app externally (e.g. outside render/locally), use this connection string instead:
    # con_string = 'postgresql://assetmappr_db_user:hyx8dhtgdq6mvyIfe3ANC2O7ceRheEr5@dpg-c9rao5j97ej5m8i836r0-a.ohio-postgres.render.com/assetmappr_db'

    # Establish connection with database (details found in Heroku dashboard after login)
    conn = psycopg2.connect(con_string)
    
    # Create cursor object
    cursor = conn.cursor()
    
    # Create a UID for the rating
    staged_rating_id = str(uuid.uuid4())
    
    rating_scale = rating_score
    comments = rating_comments
    user_community = 123 # to be generalised
    generated_timestamp = datetime.now()
    
    # Write info into staged ratings table
    cursor.execute('''INSERT INTO staged_ratings (staged_rating_id, asset_id, user_community, generated_timestamp,
                   rating_scale, comments)
                 VALUES ('{}', '{}', {}, TIMESTAMP '{}', {}, '{}');'''.format(staged_rating_id, asset_id, user_community,
                 generated_timestamp, rating_scale, comments))
    
    conn.commit()
    conn.close()
    
    return None
