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
