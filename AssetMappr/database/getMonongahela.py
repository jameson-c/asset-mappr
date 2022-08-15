"""
File: getMonongahela.py
Author: Mihir Bhaskar

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
        keyword_file: file that stores the desired keywords to pull from Google Maps API
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

if __name__ == '__main__':
    
    '''
    NATIONAL data input for the community
    '''
    # Google Data
    keyword_file = 'National/google_keywords/Monongahela_keywords.csv'
    apikey = input('Enter your Google Places API Key: ')
    lat = '40.1955304' # obtained from center of incorporated place as sourced below
    lon = '-79.9222298'
    radius = '6000'
    
    # NCES Schools API, Hospitals via Community Benefit Insights uses similar inputs
    countyFIPS = '42125'
    state = 'PA'
    countyName = 'Washington County'
    
    nationalData = national.genNatData(countyFIPS,countyName,state,# Colleges, HS, Elementary, Hospitals
                                       keyword_file, apikey, lat, lon, radius) # Google API

    # Incorporated Place GEOID
    # Sourced from https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress?form
    nationalData['community_geo_id'] = 4250408

    '''
    STATE data input for the community
    '''
    '''
    LOCAL data input for the community
    '''
    '''
    Generating Asset Metadata
    '''
 
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