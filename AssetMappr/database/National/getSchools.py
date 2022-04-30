"""
File: getSchools.py
Author: Jameson Carter

Desc: This file gets three types of schools: public primary and secondary schools,
private schools, and colleges from the Edge OpenData API:
    - https://data-nces.opendata.arcgis.com/datasets/postsecondary-school-locations-current-1/api
    - https://data-nces.opendata.arcgis.com/datasets/public-school-characteristics-2019-20/api
    - https://data-nces.opendata.arcgis.com/datasets/private-school-locations-2019-20/api

Finally, the file outputs a .csv file that contains all of the school data

Inputs: Google Places API key
Output: pandas dataframe Schools, written to .csv
"""
import pandas as pd
import time
import requests
import json

'''
Func: getPostSecSchools
Input: 
    countyFIPS: 5 digit county code we are interested in pulling schools for, which
            can be found at the url below - str
            https://www.nrcs.usda.gov/wps/portal/nrcs/detail/national/home/?cid=nrcs143_013697
            
                     
Output: A pandas dataframe containing post secondary schools in
        our standard format: 
        name	category	vicinity	latitude	longitude	website
'''

def getPostSecSchools(countyFIPS):
    
    countyFIPS = str(countyFIPS)
    
    url = ('https://services1.arcgis.com/Ua5sjt3LWTPigjyD/arcgis/rest/services/'
    'Postsecondary_School_Locations_Current/FeatureServer/0/'
    'query?where=CNTY%20%3D%20\'' + countyFIPS + 
    '\'&outFields=NAME,STREET,CITY,LAT,LON&outSR=4326&f=json')
    
    
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
        

'''
Func: getPubSchools
Input: 
    countyname: name of the county we are searching in. Note this has to exactly 
                match how it is stored in the API. Find correct spelling by 
                seeing the site below- str
                https://data-nces.opendata.arcgis.com/datasets/nces::public-school-characteristics-2019-20/explore?location=36.667912%2C-96.401190%2C16.00
    state: 2-letter abbreviation of the state we are searching in- str
                     
Output: A pandas dataframe containing post secondary schools in
        our standard format: 
        name	category	vicinity	latitude	longitude	website
'''
def getPubSchools(countyname, state):
    state = state.upper()
    
    url = ('https://nces.ed.gov/opengis/rest/services/K12_School_Locations/'
    'EDGE_ADMINDATA_PUBLICSCH_1920/MapServer/0/'
    'query?where=STABR%20%3D%20\'' + state + 
    '\'%20AND%20NMCNTY%20%3D%20\'' + countyname +
    '\'&outFields=SCH_NAME,SCHOOL_LEVEL,LATCOD,LONCOD,SCHOOL_TYPE_TEXT,SY_STATUS_TEXT,LSTREET1,LCITY,NMCNTY,STABR&outSR=4326&f=json')

    # Call the EDGE OpenData API
    response = requests.get(url)
    result = json.loads(response.text)
    df = pd.json_normalize(result['features']) # normalize json file into pandas
    
    if not df.empty: # If there ARE results, continue
        # drop unnecessary files, add category column
        # df.drop(['geometry.x', 'geometry.y'],axis = 1)  
        df['category'] = 'Public Elementary and High Schools'
        df['website'] = ''
        df.rename(columns={'attributes.SCH_NAME': 'name',
                       'attributes.LSTREET1': 'vicinity',
                       'attributes.LCITY': 'city',
                       'attributes.LATCOD': 'latitude',
                       'attributes.LONCOD': 'longitude'}, inplace = True)
    
        df['vicinity'] = df['vicinity'] + ', ' + df['city']
    
        df = df[['name','category','vicinity','latitude','longitude','website']]
    
        return df
    
    else: # Otherwise, return empty dataframe
        column_names = ['name','category','vicinity','latitude','longitude','website']
        df = pd.DataFrame(columns = column_names)
        return df
'''
Func: getPrivSchools
Input: 
    countyFIPS: 5 digit county code we are interested in pulling schools for, which
            can be found at the url below - str
            https://www.nrcs.usda.gov/wps/portal/nrcs/detail/national/home/?cid=nrcs143_013697
            
                     
Output: A pandas dataframe containing post secondary schools in
        our standard format: 
        name	category	vicinity	latitude	longitude	website
'''
def getPrivSchools(countyFIPS):
    
    countyFIPS = str(countyFIPS)

    url = ('https://nces.ed.gov/opengis/rest/services/K12_School_Locations/'
    'EDGE_GEOCODE_PRIVATESCH_1920/MapServer/0/'
    'query?where=CNTY%20%3D%20\'' + countyFIPS +
    '\'&outFields=NAME,STREET,CITY,LAT,LON&outSR=4326&f=json')

    # Call the EDGE OpenData API
    response = requests.get(url)
    result = json.loads(response.text)
    df = pd.json_normalize(result['features']) # normalize json file into pandas
    
    if not df.empty: # If there ARE results, continue
        # drop unnecessary files, add category column
        # df.drop(['geometry.x', 'geometry.y'],axis = 1)  
        df['category'] = 'Private Elementary and High Schools'
        df['website'] = ''
        df.rename(columns={'attributes.NAME': 'name',
                       'attributes.STREET': 'vicinity',
                       'attributes.CITY': 'city',
                       'attributes.LAT': 'latitude',
                       'attributes.LON': 'longitude'}, inplace = True)
    
        df['vicinity'] = df['vicinity'] + ', ' + df['city']
    
        df = df[['name','category','vicinity','latitude','longitude','website']]
    
        return df
    
    else: # Otherwise, return empty dataframe
        column_names = ['name','category','vicinity','latitude','longitude','website']
        df = pd.DataFrame(columns = column_names)
        return df

def getAllSchools(countyFIPS,countyName,state):
    
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

        