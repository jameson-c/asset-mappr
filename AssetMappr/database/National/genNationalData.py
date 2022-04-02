"""
File: GetNationalData.py
Author: Jameson Carter

Desc: This file calls all of the functions collecting national datasets 

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
import getSchools
import getGoogle
import pandas as pd

def genNatData(countyFIPS,countyName,state,# Colleges, Pub/Private HS, Elementary
               apiKey, lat, long, radius # Google API
            ):
    
    private, public, college = getSchools.getAllSchools(countyFIPS,countyName,state)
    google = getGoogle.createGoogleDF(apiKey, lat, long, radius)
    
    frame = pd.concat([private, public, college,
                       google])
    
    return frame
                            


    
