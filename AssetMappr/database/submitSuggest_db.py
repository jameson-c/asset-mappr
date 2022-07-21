"""
File: submitSuggest_db.py
Author: Anna Wang

Desc: Interacts with the database to write suggestion edit for asset information to the suggested_edits table;

Input:
    - (str) edit_id: unique id of suggestion edit
    - (str) asset_id: the asset ID to which the suggestion pertains 
    - (str) suggested_name: the asset's suggested name
    - (str) suggested_desc: the asset's suggested description
    - (str) suggested_address: the asset's suggested address
    - (str) suggested_category: the asset's suggested category
    - (str) suggested_website: the asset's suggested website
    - (str) current_status: the asset's current status: temporarily closed, permanently closed, does not exist here
    - (str) user_upoload_ip: ip address of the user
   
Output: 
    - None: this function only writes to the SQL database directly
    
"""
import psycopg2
import uuid
from datetime import datetime
import requests
import json
import os


def submitSuggest_db(edit_id, asset_id, name, desc, address, category, website, status, ip):

    # When deploying on Render, use this string
    # con_string = 'postgresql://assetmappr_database_user:5uhs74LFYP5G2rsk6EGzPAptaStOb9T8@dpg-c9rifejru51klv494hag-a/assetmappr_database'

    # If running the app externally (e.g. outside render/locally), use this connection string instead:
    con_string = os.getenv('db_uri')

    # Establish connection with database (details found in Heroku dashboard after login)
    conn = psycopg2.connect(con_string)

    # Create cursor object
    cursor = conn.cursor()

    # Create a UID for the rating
    edit_id = str(uuid.uuid4())
    asset_id = asset_id
    suggested_asset_name = name
    suggested_description = desc
    suggested_address = address

    # get lat lon from google API
    google_api_key = 'AIzaSyDitOkTVs4g0ibg_Yt04DQqLaUYlxZ1o30'
    
    # Need to generalise this
    address = address + ' Uniontown, PA'

    params = {'key': google_api_key,
              'address': suggested_address}
    url = 'https://maps.googleapis.com/maps/api/geocode/json?'

    response = requests.get(url, params)
    result = json.loads(response.text)

    suggested_latitude = result['results'][0]['geometry']['location']['lat']
    suggested_longitude = result['results'][0]['geometry']['location']['lng']

    suggested_website = website
    current_status = status
    suggested_category = category

    generated_timestamp = datetime.now()

    user_upload_ip = ip

    # Write info into suggested_edits table
    cursor.execute('''INSERT INTO suggested_edits (edit_id, asset_id, suggested_asset_name, suggested_description, suggested_address, suggested_latitude, suggested_longitude ,suggested_website,
                   current_status, suggested_category, user_upload_ip, generated_timestamp) VALUES('{}','{}','{}', '{}','{}',{},{},'{}', '{}','{}','{}',TIMESTAMP'{}');'''.format(
        edit_id, asset_id, suggested_asset_name, suggested_description, suggested_address, suggested_latitude, suggested_longitude, suggested_website, current_status, suggested_category, user_upload_ip, generated_timestamp))

    conn.commit()
    conn.close()

    return None
