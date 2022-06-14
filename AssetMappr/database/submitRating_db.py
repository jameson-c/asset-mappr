"""
File: submitRating_db.py
Author: Anna Wang, Mihir Bhaskar

Desc: Interacts with the database to write ratings to the staged ratings table

Input:
    - (str) ip: the IP address from which the user is uploading the rating
    - (str) asset_id: the asset ID to which the rating pertains 
    - (int) rating_score: score selected on scale of 0-5
    - (str) rating_comments: text string with any comments the user gave in the review
    - (int) community_geo_id: the relevant community geo ID
   
Output: 
    - None: this function only writes to the SQL database directly
    
"""
import psycopg2
import uuid
from datetime import datetime

def submitRating_db(ip, asset_id, rating_score, rating_comments, community_geo_id):
    
    # When deploying on Render, use this string
    # con_string = 'postgresql://assetmappr_database_user:5uhs74LFYP5G2rsk6EGzPAptaStOb9T8@dpg-c9rifejru51klv494hag-a/assetmappr_database'
    
    # If running the app externally (e.g. outside render/locally), use this connection string instead:
    con_string = 'postgresql://assetmappr_database_user:5uhs74LFYP5G2rsk6EGzPAptaStOb9T8@dpg-c9rifejru51klv494hag-a.ohio-postgres.render.com/assetmappr_database'

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
    
    # Write info into staged ratings table
    cursor.execute('''INSERT INTO staged_ratings (user_upload_ip, staged_rating_id, asset_id, user_community, generated_timestamp,
                   rating_scale, comments)
                 VALUES ('{}','{}', '{}', {}, TIMESTAMP '{}', {}, '{}');'''.format(user_upload_ip, staged_rating_id, asset_id, user_community,
                 generated_timestamp, rating_scale, comments))
    
    conn.commit()
    conn.close()
    
    return None
