"""
File: populateDB.py
Author: Jameson Carter

Desc: This file populates the Render PostGres database with pre-populated assets. 
      Additionally, it checks to see if master tables are inconsistent with incoming data
      Finally, it provides a method for populating the master tables.

Inputs: 
    cursor: a psychopg2-initialized cursor with connection to our database
    data: the data generated through getUniontown.py
        
Output: either committed changes to our database, or nothing.
"""

import pandas as pd
import psycopg2
import psycopg2.extras as extras
import psycopg2.sql as sql

'''
Func: checkMasterTables
Input: 
    cursor: a psychopg2-initialized cursor with connection to our database
    data: the data generated through getUniontown.py

Output: Boolean True or False, delineating whether master tables are in good shape
to handle incoming dataset.
'''
def checkMasterTables(data, conn):

    cursor = conn.cursor()
    # What communities are in the master table now?
    get_Communities_ms = "select * from communities_master"
    cursor.execute(get_Communities_ms)
    communities_res = cursor.fetchall()
    
    communities_ms = set([tup[0] for tup in communities_res])
    
    # What categories are in the master table now?
    get_Categories_ms = "select * from categories_master"
    cursor.execute(get_Categories_ms)
    categories_res = list(cursor.fetchall())
    categories_ms = set([tup[0] for tup in categories_res])
    
    # What sources are in the master table now?
    get_Sources_ms = "select * from sources_master"
    cursor.execute(get_Sources_ms)
    sources_res = list(cursor.fetchall())
    sources_ms = set([tup[0] for tup in sources_res])
    
    # Get unique categories in incoming data
    unique_cats = set(data['category'])
    diff_cats = unique_cats.difference(categories_ms)
    
    # Get unique sources in incoming data
    unique_sources = set(data['source_type'])
    print(unique_sources)
    print(data)
    print(sources_ms)
    diff_sources = unique_sources.difference(sources_ms)
    
    # Get unique communities in incoming data
    unique_community = set(data['community_geo_id'])
    diff_community = unique_community.difference(communities_ms)

    # IF these do not already exist in the category table, submit them!
    # If they do not, do not submit them. Master tables must contain all categories
    print("These categories are in the master table:\n")
    print(categories_ms)
            
    print("\nThese sources are in the master table:\n")
    print(sources_ms)
            
    print("\nThese community GEOIDs are in the master table:\n")
    print(communities_ms)
    
    if len(diff_cats)>0 or len(diff_sources)>0  or len(diff_community)>0:
        print("\nThese categories are in the data, but not in the master table:")
        for cat in diff_cats:
            print(cat)
            
        print("\nThese sources are in the data, but not in the master table:")
        for source in diff_sources:
            print(source)
            
        print("\nThese community GEOIDs are in the data, but not in the master table:")
        for community in diff_community:
            print(community)
        
        print('\nAny discrepancies above MUST BE RESOLVED before proceeding')
        cursor.close()
        return False
    
    print('No discrepancies found between master tables and incoming data')
    cursor.close()
    return True

'''
Func: populateMasterTables
Input: 
    cursor: a psychopg2-initialized cursor with connection to our database
    data: the data generated through getUniontown.py

Output: changes commited to Render DB maaster tables.

CHANGE THIS and run manually if master tables need to be updated.
'''    
def populateMasterTables(conn):

    # Create the record that will be used to populate the community master file
    community_master = pd.DataFrame([[4278528, 'Uniontown', 'C5', '39.8993024', '-79.7245287']],
                                    columns = ['community_geo_id',
                                               'community_name',
                                               'community_class_code',
                                               'latitude',
                                               'longitude'])
    
    # Create the record that will be used to populate the source master file
    source_master = pd.DataFrame([['NCES Common Core of Data API'],
                                     ['Community Benefit Hospitals API'],
                                     ['Google API']],
                                    columns = ['source_type'])
    
    # Create the record that will be used to populate the categories master file
    category_master = pd.DataFrame([['Sports and recreation'],
                                    ['Culture and history'],
                                    ['Education and workforce development'],
                                    ['Healthcare'],
                                    ['Housing'],
                                    ['Places of worship'],
                                    ['Community service and assistance'],
                                    ['Transport and infrastructure'],
                                    ['Food access'],
                                    ['Nature and parks'],
                                    ['Libraries'],
                                    ['Economic development opportunities'],
                                    ['Local business and economy']],
                                    columns = ['category'])
    
    # Create the record that will be used to populate the values master file
    values_master = pd.DataFrame([['Needs renovation', 'Negative'],
                                  ['Services need improvement', 'Negative'],
                                  ['Needs maintenance/clean-up', 'Negative'],
                                  ['Physical space should be used differently', 'Negative'],
                                  ['Harmful for the community', 'Negative'],
                                  ['Good for family/kids', 'Positive'],
                                  ['Good for community spirit', 'Positive'],
                                  ['Fond memories', 'Positive'],
                                  ['Great services provided', 'Positive'],
                                  ['Useful in daily life', 'Positive'],
                                  ['Visually pleasing or beautiful', 'Positive'],
                                  ['Entertaining/fun', 'Positive']],
                                  columns=['value', 'value_type'])
    
    # categories_master
    execute_values(conn, category_master, 'categories_master')
    
    # sources_master
    execute_values(conn, source_master, 'sources_master')
    
    # communities_master
    execute_values(conn, community_master, 'communities_master')
    
    # values_master
    execute_values(conn, values_master, 'values_master')
   
'''
Func: execute_values
Input: 
    conn: a psychopg2-initialized cursor with connection to our database
    data: the data generated through getUniontown.py
Source: https://naysan.ca/2020/05/09/pandas-to-postgresql-using-psycopg2-bulk-insert-performance-benchmark/
Output: changes commited to Render DB master tables.
'''   
def execute_values(conn, df, table):
    """
    Using psycopg2.extras.execute_values() to insert the dataframe
    """
    # Create a list of tupples from the dataframe values
    tuples = [tuple(x) for x in df.to_numpy()]
    # Comma-separated dataframe columns
    cols = ','.join(list(df.columns))
    # SQL quert to execute
    query  = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return
    print("execute_values() done")
    cursor.close()
'''
Func: track_exists
Input: 
    cursor: a psychopg2-initialized cursor with connection to our database
    data: the data generated through getUniontown.py
    curr_community: community geoid tracking the community we are populating

Output: changes commited to Render DB.
'''
def track_exists(cursor, asset_name, address, latitude, longitude):
    query = ("SELECT asset_name, address, latitude, longitude "
                "FROM assets WHERE asset_name = %s OR address = %s "
                "OR latitude = %s AND longitude = %s")
    
    vals = (asset_name, address, latitude, longitude)

    cursor.execute(query, vals)
    return cursor.fetchone() is not None

'''
Func: populateDB
Input: 
    cursor: a psychopg2-initialized cursor with connection to our database
    data: the data generated through getUniontown.py
    curr_community: community geoid tracking the community we are populating
    
This must insert into assets. One essential question- what happens if we try to 
populate something into the table that already exists? How do we delineate between
new assets and assets that represent the same location, especially after ratings 
are added? One way of doing this is to check lat == lat and lon == lon

Then, we only insert the rows which are not duplicative. This means we do not overwrite
existing assets, unless their lat/lon points change. Or unless two assets share
the same location, which is possible... So maybe when lat/lon match I prompt
the user and let them know, showing the asset currently in that location. If 
that asset is not problematic, insert. Otherwise exclude it. This way the uuids 
do not get overwritten, either.

Output: changes commited to Render DB.
'''
def populateDB(data, conn):
    
    cursor = conn.cursor()
    extras.register_uuid()
    # What assets are in the master table now, for this community?
    # tuple format ex: [(4278528, 'Uniontown', 'C5', 39.8993024, -79.7245287)]
    '''
    potential_dupes = []
    for index, row in data.iterrows():
        result = track_exists(cursor, row['asset_name'],
                             row['address'],
                             row['latitude'],
                             row['longitude'])
        potential_dupes.append(result)
    print(potential_dupes)
    '''
    '''
    insert contingency
    '''
    categories = data[['asset_id', 'category']]
    data = data[['asset_id', 'asset_name','description','asset_type', 'community_geo_id',
                 'source_type', 'website', 'latitude','longitude','address',
                 'generated_timestamp']]
    execute_values(conn, data, 'assets')
    execute_values(conn, categories, 'asset_categories')

    '''
    
if __name__ == '__main__':
    con_string = 'postgres://postgres:r]H,lQOEiRcxqMcM21!Q@localhost:5432/postgres'
    # Establish connection with database
    conn = psycopg2.connect(con_string)
    data = pd.read_csv('C:/Users/jacar/OneDrive/Documents/GitHub/asset-mappr/AssetMappr/database/NationalData.csv')
    populateDB(data, conn)
    '''