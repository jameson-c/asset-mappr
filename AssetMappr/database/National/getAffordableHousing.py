"""
File: getAffordableHousing.py
Author: Jameson Carter

Desc: This file gets housing projects across the US from the HUD API:
    - LIHTC: https://hudgis-hud.opendata.arcgis.com/datasets/HUD::low-income-housing-tax-credit-properties/api
    - Public Housing: 

Finally, the file outputs a pandas dataframe that contains all of the hospital data.


Inputs: Google Places API key, state-county code abbreviation 
Output: pandas dataframe df returned
"""
import pandas as pd
import requests
import json
import geopandas as gpd
import contextily as ctx
import matplotlib.pyplot as plt

def getLIHTC(CtyFIPS):
    
    if len(CtyFIPS) == 5:
        county = CtyFIPS[3:]
        state = CtyFIPS[0:2]
    else:
        county = CtyFIPS[2:]
        state = CtyFIPS[0:2]
    
    url = ('https://services.arcgis.com/VTyQ9soqVukalItT/arcgis/rest/services/LIHTC/FeatureServer/0/query?where=STATE2KX%20%3D%20'
           + state + '%20AND%20CNTY2KX%20%3D%20' + county + 
           '&outFields=LAT,LON,PROJ_ADD,PROJ_CTY,PROJECT,CNTY2KX,STATE2KX&outSR=4326&f=json')
    
    response = requests.get(url)
    result = json.loads(response.text)
    df = pd.json_normalize(result['features']) 
    
    
    df = df.rename(columns={'attributes.PROJ_ADD':'address', 
                       'attributes.LAT' : 'latitude',
                       'attributes.LON' : 'longitude',
                       'attributes.PROJECT' : 'asset_name'})
    
    df['category'] = 'Housing'
    df['website'] = ''
    df['source_type'] = 'HUD API'
    df['asset_name'] = df['asset_name'].str.title()
    
    
    df = df[['asset_name','category','address','latitude','longitude','website','source_type']]
    
    return df

def getPublicHousing(CtyFIPS):
    
    if len(CtyFIPS) == 5:
        county = CtyFIPS[3:]
        state = CtyFIPS[0:2]
    else:
        county = CtyFIPS[2:]
        state = CtyFIPS[0:2]
    
    url = ('https://services.arcgis.com/VTyQ9soqVukalItT/arcgis/rest/services/Public_Housing_Buildings/FeatureServer/0/query?where=STATE2KX%20%3D%20'
           + state + '%20AND%20CNTY2KX%20%3D%20' + county + 
           '&outFields=PROJECT_NAME,CNTY_NM2KX,CNTY2KX,STD_CITY,STD_ST,LAT,LON,STATE2KX,STD_ADDR&outSR=4326&f=json')
    
    response = requests.get(url)
    result = json.loads(response.text)
    df = pd.json_normalize(result['features']) 
    
    
    df = df.rename(columns={'attributes.STD_ADDR':'address', 
                       'attributes.LAT' : 'latitude',
                       'attributes.LON' : 'longitude',
                       'attributes.PROJECT_NAME' : 'asset_name'})
    
    df['category'] = 'Housing'
    df['website'] = ''
    df['source_type'] = 'HUD API'
    df['asset_name'] = df['asset_name'].str.title()
    
    
    df = df[['asset_name','category','address','latitude','longitude','website','source_type']]
    
    return df

if __name__ == '__main__':
    df = getLIHTC('42051')
    df2 = getPublicHousing('42051')
    gdf = gpd.GeoDataFrame(df2, 
                           crs = 'EPSG:3857',
                           geometry=gpd.points_from_xy(df2.longitude, df2.latitude))
    ax = gdf.boundary.plot(figsize=(20, 20), alpha=1.0, edgecolor='blue')
    ctx.add_basemap(ax, crs=gdf.crs.to_string())
    ax.set_axis_off()
    plt.show()
    