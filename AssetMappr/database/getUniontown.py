"""
File: main.py
Author: Jameson Carter

Desc: This file calls the state, local, and national scripts to populate the 
      Heroku database with pre-populated assets. 

Inputs: 
    School Data:
        countyFIPS: 5 digit county code found at the url below 
            https://www.nrcs.usda.gov/wps/portal/nrcs/detail/national/home/?cid=nrcs143_013697
        countyName: name of the county we are searching in. Note this has to exactly 
            match how it is stored in the API, as in the site below:
            https://data-nces.opendata.arcgis.com/datasets/nces::public-school-characteristics-2019-20/explore?location=36.667912%2C-96.401190%2C16.00
        state: 2 digit state acronym. Example: PA
    Google Data:
        apikey: Google Places API key
        lat: latitude
        long: longitude
        radius: radius around which to search for data
Output: pandas dataframe Schools, written to .csv
"""

import pandas as pd
import National.genNationalData as national
# import getStateData
# import getLocalData
import psycopg2
'''
# Establish connection with database (details found in Render dashboard after login)



Goal of this file is to:
    1. Check to ensure assets are not duplicated. If they are:
        a. check to see if duplication was intended. Is this an update?
    2. Populate to the following tables:
        a. Assets:
            Asset_ID
            Source_Type
            Community_GEOID
        b. Asset_Categories:
            Asset_ID
            Category_ID
        c. Communities_Master
            Community_GEOID
        d. Sources_Master
            Source_Type
    3. Check to see if the values in master tables are already present. In 
    case of community master, do nothing. In case of sources_master, check to 
    see if the source, for this community, is already used. Ask if data is being 
    updated. If not, then do not overwrite.
    4. If a given source type and community ID has been assigned, that suggests
       asset is new. 
    6. Do not overwrite asset in Assets if you are updating, but the name differs.


cursor = conn.cursor()
cursor.execute(createdb)
createdb = 
SQL

conn.commit()
'''

if __name__ == '__main__':
    
    '''
    NATIONAL data input for the community
    '''
    # Google Data- Social Benefit
    apikey = input('Enter your Google Places API Key: ')
    lat = '39.8993885'
    long = '-79.7249338'
    radius = '6000'
    
    # NCES Schools API
    countyFIPS = '42051'
    state = 'PA'
    countyName = 'Fayette County'
    
    nationalData = national.genNatData(countyFIPS,countyName,state,# Colleges, HS, Elementary
                                       apikey, lat, long, radius) # Google API
    
    nationalData.to_csv('NationalData.csv') # Output file
    