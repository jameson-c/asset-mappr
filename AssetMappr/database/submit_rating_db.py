import psycopg2
import uuid
from datetime import datetime

def submit_rating_db(asset_id, rating_score, rating_comments):
    
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
    
    # Process info
    staged_rating_id = str(uuid.uuid4())
    
    rating_scale = rating_score
    comments = rating_comments
    user_community = 123
    generated_timestamp = datetime.now()
    
    # Write info into staged ratings table
    cursor.execute('''INSERT INTO staged_ratings (staged_rating_id, asset_id, user_community, generated_timestamp,
                   rating_scale, comments)
                 VALUES ('{}', '{}', {}, TIMESTAMP '{}', {}, '{}');'''.format(staged_rating_id, asset_id, user_community,
                 generated_timestamp, rating_scale, comments))
    
    conn.commit()
    conn.close()
    
    return None
