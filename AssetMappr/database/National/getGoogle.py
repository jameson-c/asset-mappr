"""
File: getGoogleData.py
Author: Jameson Carter, Michaela Marincic

Desc: This file uses the getMapData function to call the google API and
search our keywords within a 50000 meter radius of the center of Pittsburgh, 
covering well beyond the entire area of Pittsburgh. Then, the file removes 
suspected restaurants and storesand drops duplicate results from respective 
keyword searches. Then, the file uses the getLocationWebsite function to attach
website information to the places which have a website.

Finally, the file outputs a .csv file that contains all of the Google API data
that we need.

Inputs: Google Places API key
Output: pandas dataframe MainFrame, written to .csv
"""
import pandas as pd
import time
import requests
import json

def getMapData(key, location, keyword, radius, next_page_token = None):
    params = {
        'key' : key,
        'location' : location,
        'keyword' : keyword,
        'radius' : radius,
        'pagetoken' : next_page_token
        }
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
    # If there is no next page token provided, delete that key-value pair
    if next_page_token is None:
        del params['pagetoken']
    # Call the Google API
    response = requests.get(url,params)
    result = json.loads(response.text)
    df = pd.json_normalize(result['results'])
    # Separate the address from the city, first add commas to strings without
    # them so that we can use str.split()
    df = df.loc[:,df.columns.isin(['geometry.location.lat','geometry.location.lng',
            'vicinity','name','place_id','price_level',])]

    # Rename to make everything simpler
    df = df.rename(columns={"geometry.location.lat": "latitude", 
                       "geometry.location.lng": "longitude", 
                       "vicinity": "address"})
    # Finally, return the next page token for the next page, if there is one
    try:
        next_page_tk = result['next_page_token']
        return [df,next_page_tk]
    except:
        # Return the output data frame and the next page token in a list
        return [df,None]


def getLocationWebsite(key, ID, fields):
    params = {'key' : key,
              'place_id' : ID,
              'fields' : fields}
    url = 'https://maps.googleapis.com/maps/api/place/details/json?'
    response = requests.get(url,params)
    result = json.loads(response.text)
    df = pd.json_normalize(result['result'])
    return df

def createGoogleDF(keyword_file, apiKey, lat, long, radius):
    with open(keyword_file, 'r') as f:
        keywords = []
        categories = []
        for line in f:
            line = line.split(',')
            keywords.append(line[1])
            categories.append(line[0])

    MainFrame = pd.DataFrame()
    catIndex = 1
    latlong = ','.join([lat, long])
        
    for keyword in keywords[1:]:
    
        results = getMapData(apiKey,
                               latlong, keyword, radius)
                
        data = results[0]
        data['category'] = categories[catIndex]
        nextToken = results[1]
        
        # Next, we run the query again on up to two nextToken calls. 
        # Google's API only produces 60 results on nearby search, with 20 in each
        # initial API call. So we check to see whether there is a nextToken for each
        if nextToken is not None:
            time.sleep(2) # Need to introduce this so that API call ready for token
            results2 = getMapData(apiKey,
                               latlong, keyword, radius, 
                               nextToken)
            data2 = results2[0]
            data2['category'] = categories[catIndex]
            nextToken = results2[1]
        
            if nextToken is not None:
                time.sleep(2)
                results3 = getMapData(apiKey,
                               latlong, keyword, radius, 
                               nextToken)
                data3 = results3[0]
                data3['category'] = categories[catIndex]
                nextToken = results3[1]
                
       # This portion of the code appends data to data2 and data3, if both 
       # exist, to data2 if data3 does not exist, and to nothing if neither
       # exist. The variable data should always exist.
        try:
            # MainFrame = MainFrame.append([data, data2, data3], ignore_index = True)
            MainFrame = pd.concat([MainFrame, data, data2, data3], ignore_index=True)
        except:
            try:
                # MainFrame = MainFrame.append([data, data2], ignore_index = True)
                MainFrame = pd.concat([MainFrame, data, data2], ignore_index=True)

            except:
                # MainFrame = MainFrame.append([data], ignore_index = True)
                MainFrame = pd.concat([MainFrame, data], ignore_index=True)

    
        # Tick up the index for 'categories' to get the category for the next keyword.        
        catIndex += 1

   
    # Retain addresses
    # MainFrame = MainFrame[MainFrame['address'].str.contains('Pittsburgh')]
    # Drop results with a price level listed (Gets rid of most of the restaurants)
    MainFrame = MainFrame.drop(MainFrame.loc[MainFrame['price_level']>=1].index)
    
    # Drop price level, if it exists
    MainFrame['asset_name'] = MainFrame['name']
    MainFrame = MainFrame.loc[:,MainFrame.columns.isin(['latitude','longitude',
            'address','asset_name','place_id','category',])]
    
    # 'URL' column will be added using Google Maps API "Place Details"
    websites = {'place_id':[], 'website':[]}
    for i in MainFrame['place_id']:
        result = getLocationWebsite(apiKey,
                                        i,'website')
    
        if not result.empty:
            websites['place_id'].append(i)
            websites['website'].append(result.at[0,'website'])
    websitedf = pd.DataFrame.from_dict(websites)

    MainFrame = MainFrame.join(websitedf.set_index('place_id'), on='place_id')
    MainFrame.drop(columns = 'place_id', inplace = True)
    
    # Drop duplicates
    MainFrame = MainFrame.drop_duplicates()
    
    # Establish Source:
    MainFrame['source_type'] = 'Google API' 
    
    # Add a description field
    MainFrame['description'] = ''
    
    return MainFrame