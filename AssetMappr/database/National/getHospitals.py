"""
File: getHospitals.py
Author: Michaela Marincic

Desc: This file gets hospitals across the US from the Community Benefit API:
    - About: https://www.communitybenefitinsight.org/?page=info.data_api
    - API: http://www.communitybenefitinsight.org/api/get_hospitals.php

Finally, the file outputs a .csv file that contains all of the hospital data

THIS IS COPIED FROM JAMIE AS A TEMPLATE - STILL NEED TO UPDATE


Inputs: Google Places API key
Output: pandas dataframe Schools, written to .csv
"""
import pandas as pd
import time
import requests
import json

'''
Func: getHospitals
Input: 
    countyFIPS: 5 digit county code we are interested in pulling schools for, which
            can be found at the url below - str
            https://www.nrcs.usda.gov/wps/portal/nrcs/detail/national/home/?cid=nrcs143_013697
            
                     
Output: A pandas dataframe containing post secondary schools in
        our standard format: 
        name	category	vicinity	latitude	longitude	website
'''

def getHospitals(twoLetterState):
    
    stateCode = str(twoLetterState)
    
    url = ('http://www.communitybenefitinsight.org/api/get_hospitals.php'
    '?state=' + stateCode)
    
    
    # Call the EDGE OpenData API
    response = requests.get(url)
    result = json.loads(response.text)
    df = pd.json_normalize(result['features']) # normalize json file into pandas
    if not df.empty: # If there ARE results, continue
        # drop unnecessary files, add category column
        # df.drop(['geometry.x', 'geometry.y'],axis = 1)  
        df['category'] = 'Postsecondary Schools'
        df['website'] = ''
        df.rename(columns={'attributes.NAME': 'name',
                       'attributes.STREET': 'vicinity',
                       'attributes.CITY': 'city',
                       'attributes.LAT': 'latitude',
                       'attributes.LON': 'longitude'}, inplace = True)
    
        df['vicinity'] = df["vicinity"] + ', ' + df["city"]
    
        df = df[['name','category','vicinity','latitude','longitude','website']]
    
        return df
    
    else: # Otherwise, return empty dataframe
        column_names = ['name','category','vicinity','latitude','longitude','website']
        df = pd.DataFrame(columns = column_names)
        return df
        


def getAllSchools(countyFIPS,countyName,state):
    #countyFIPS = input('Look at this site to find the county code you are searching for: https://www.nrcs.usda.gov/wps/portal/nrcs/detail/national/home/?cid=nrcs143_013697\n\nEnter the 5-digit county FIPS code: ')
    #state = input('Enter the 2-letter state abbreviation: ')
    #countyName = input('Look at this site and find how the county name is spelled word for word (including the word county, sometimes), case sensitive: https://data-nces.opendata.arcgis.com/datasets/nces::public-school-characteristics-2019-20/explore?location=36.666724%2C-96.405824%2C16.00\n\nEnter County Name: ')
    s
    private = getPrivSchools(countyFIPS)
    public = getPubSchools(countyName,state)
    college = getPostSecSchools(countyFIPS)
    
    print('\nIf any of these searches yield no results, make sure your county names, county codes, and state codes are correct')
    print(f'We found {len(private)} private schools')
    print(f'We found {len(public)} public schools')
    print(f'We found {len(college)} postsecondary schools')
    
    return private, public, college
    
    #Schools = private.append(public, ignore_index = True).append(college, ignore_index = True)
    
    #Schools.to_csv('Schools.csv')

        