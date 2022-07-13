"""
File: cleanStaged.py
Author: Mihir Bhaskar

Desc: This file cleans the user-inputted data coming into staged assets and ratings, moving
      the verified content into the main 'assets' and 'ratings' tables.

Inputs: 

TODO:
- Add location comparison / other more nuanced cleaning
- Decide whether we want to have the cleaning as community-specific    

"""
import pandas as pd
import psycopg2
from populateDB import populateDB

def cleanStaged(con_string):
    '''
    This function reads staged_assets, staged_asset_categories, staged_ratings, and staged_values,
    performs some cleaning 
    
    Input: a connection string (URI) for the database
    '''
    
    # Reading in staged assets and staged asset categories that aren't from the 'test' communtity

    staged_assets = pd.read_sql('''SELECT * FROM staged_assets
                                   WHERE community_geo_id != 123''', con=con_string)
                                   
    if len(staged_assets) == 0:
        return "No assets to move"
                                 
    else:
        
        staged_asset_cats = pd.read_sql('''SELECT * FROM staged_asset_categories
                                        WHERE staged_asset_id IN
                                            (SELECT staged_asset_id FROM staged_assets
                                             WHERE community_geo_id != 123)
                                        ''', con=con_string)
                                        
        
        # Merge data
        asset_data = pd.merge(staged_assets, staged_asset_cats, on='staged_asset_id')
    
        # Drop where user_name is from our team
        # Team names to drop
        users_to_drop = ['Mihir', 'Jameson']
        asset_data = asset_data[~asset_data.user_name.isin(users_to_drop)]
        
        # Write these assets to main assets table
        asset_data = asset_data.rename(columns={'staged_asset_id': 'asset_id'})
        conn = psycopg2.connect(con_string)
        populateDB(asset_data, conn)
        
        # Check if there are ratings, and transfer them over
        
        # Clear the information from staged tables (ratings, asset_cats, then finall staged assets)
        for i in asset_data['asset_id']:
            query = '''DELETE FROM staged_asset_categories
                        WHERE staged_asset_id = '{}';
                        
                        DELETE FROM staged_assets
                        WHERE staged_asset_id = '{}' '''.format(i, i)
                        
            cursor = conn.cursor()
            
            cursor.execute(query)
            
        conn.commit()
        
        conn.close()
        
        return 'Staged assets moved successfully'

if __name__ == '__main__':
    cleanStaged(con_string='postgresql://assetmappr_database_user:5uhs74LFYP5G2rsk6EGzPAptaStOb9T8@dpg-c9rifejru51klv494hag-a.ohio-postgres.render.com/assetmappr_database')