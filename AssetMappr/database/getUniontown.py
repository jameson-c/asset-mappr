"""
File: getUniontown.py
Author: Jameson Carter

Desc: This file calls the state, local, and national scripts to populate the 
      Render PostGres database with pre-populated assets. 

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
    Hospital Data:
        countyFIPS: 5 digit county code found at the url below 
            https://www.nrcs.usda.gov/wps/portal/nrcs/detail/national/home/?cid=nrcs143_013697
        state: 2 digit state acronym. Example: PA
        
Output: pandas dataframe Schools, written to .csv
"""
import uuid
from datetime import datetime
import pandas as pd
import National.genNationalData as national
# import getStateData
# import getLocalData
import psycopg2
from populateDB import populateDB, checkMasterTables
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
    # Google Data
    keyword_file = 'National/google_keywords/Uniontown_keywords.csv'
    
    apikey = input('Enter your Google Places API Key: ')
    lat = '39.8993024' # obtained from center of incorporated place as sourced below
    lon = '-79.7245287'
    radius = '6000'
    
    # NCES Schools API, Hospitals via Community Benefit Insights uses similar inputs
    countyFIPS = '42051'
    state = 'PA'
    countyName = 'Fayette County'
    
    nationalData = national.genNatData(countyFIPS,countyName,state,# Colleges, HS, Elementary, Hospitals
                                       keyword_file, apikey, lat, lon, radius) # Google API

    # Incorporated Place GEOID
    # Sourced from https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress?form
    nationalData['community_geo_id'] = 4278528

    '''
    STATE data input for the community
    '''
    '''
    LOCAL data input for the community
    '''
    '''
    Generating Asset Metadata
    '''
    
    # Do some basic cleaning of miscategorised/wrong assets
    wrong_cat_assets = ["DICK'S Sporting Goods", "Jan & Jeff's Discount Store",
                  "Outdoors LTD", "Rick Rafail Pool Construction", 'The Salvation Army Thrift Store & Donation Center',
                  "Walmart Home Theater Installation", 'Hutchinson Park', "Marra's Mountaineer Sport Shop"]
    
    nationalData = nationalData[~nationalData.asset_name.isin(wrong_cat_assets)]
    
    # Need to sort out duplicates that arise from the same asset coming from two different sources (Maps API and getSchools/getHospitals), referring to the same category
    # For these cases, these two rows need to be collapsed into one
    # If time: sometimes, one data source will have more info than the other (e.g. website vs. no website), so if this info can also be preserved/collapsed into one row that would be great
    
    # Asset ID (uuid) needs to be created on the basis of asset name + location
    
    # There are cases where the asset name is the same, but there could be multiple locations (e.g. multiple outlets of the same store)
    # There are also cases where the location is the same, but there are two different assets in that location - e.g. an elementary school, and a middle school by different names
    
    # Right now, in nationalData, there are multiple rows for the same asset if it has multiple categories, and the only thing
    # varying across these rows is the category. The same asset ID needs to be assigned for these rows referring to the same asset - right
    # now, a new uuid is created for every row in the table.
    
    # This is some nice code to look for similar locations and flag them, based on similar lat/longs:
        # https://stackoverflow.com/questions/54867061/how-to-detect-almost-duplicate-locations-in-a-pandas-dataframe
    
    # Set AssetIDs
    nationalData['asset_id'] = [uuid.uuid4() for _ in range(len(nationalData.index))]
    
    # Add Asset Types
    nationalData['asset_type'] = 'Tangible'
    
    # Add Timestamp
    nationalData['generated_timestamp'] = datetime.now()
    
    '''
    Populating the database
    '''
    # Accessing DB externally (e.g. outside render/locally), use this connection string:
    # con_string = 'postgresql://assetmappr_db_user:hyx8dhtgdq6mvyIfe3ANC2O7ceRheEr5@dpg-c9rao5j97ej5m8i836r0-a.ohio-postgres.render.com/assetmappr_db'
    con_string = 'postgres://assetmappr_database_user:5uhs74LFYP5G2rsk6EGzPAptaStOb9T8@dpg-c9rifejru51klv494hag-a.ohio-postgres.render.com/assetmappr_database'
    # Establish connection with database
    conn = psycopg2.connect(con_string)
    
    # Now check to see if master tables align with the incoming data. Do not populate if there are inconsistencies.
    result = checkMasterTables(nationalData, conn)
    dat = nationalData
    if result == True:
        populateDB(dat,conn)
    
    