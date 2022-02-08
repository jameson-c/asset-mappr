"""
File: filterNearby
Description: Function to filter the dataframe with matches within a certain distance

Next steps:
    - This function can be generalised, but for now assuming data is in a DF with lat/long columns named
    'latitude' and 'longitude'

"""
import pandas as pd
from geopy.distance import distance

def filterNearby(point, data, max_dist = 5):   
   
   # Combing lat and long columns into one column with tuples   
   data['place_coords'] = data[['LATITUDE', 'LONGITUDE']].apply(tuple, axis=1)
   
   ## Alternative code for the above - could be faster? 
   ## data['place_coords'] = list(zip(data.latitude, data.longitude))

   # Applying the distance function to each row to create new column with distances
   data['DISTANCE IN MILES'] = data.apply(lambda x: distance(point, x['place_coords']).miles, axis=1)
   
   # Return data frame filtered with rows <= the maximum distance
   return data[data['DISTANCE IN MILES'] <= max_dist]
    
    
    

