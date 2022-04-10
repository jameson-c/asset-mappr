"""
File: createDBstructure.py
Author: Mihir Bhaskar

Desc: This file creates the table structure of the Heroku postgreSQL database

Inputs: none
Outputs: New tables committed to the postgreSQL database to which the app is linked
"""

import psycopg2

# Establish connection with database (details found in Heroku dashboard after login)
conn = psycopg2.connect(
    database = #####,
    user = #####,
    password = #####,
    host = #####,
    port = #####
    )

# Create cursor object
cursor = conn.cursor()

# Dropping existing tables
cursor.execute('''
               DROP TABLE IF EXISTS assets_preloaded CASCADE;
               DROP TABLE IF EXISTS sources_master CASCADE;
               DROP TABLE IF EXISTS categories_master CASCADE;
               DROP TABLE IF EXISTS values_master CASCADE;
               DROP TABLE IF EXISTS communities_master CASCADE;

               DROP TABLE IF EXISTS assets CASCADE;
               DROP TABLE IF EXISTS asset_categories CASCADE;
               DROP TABLE IF EXISTS ratings CASCADE;
               DROP TABLE IF EXISTS values CASCADE;
               DROP TABLE IF EXISTS missing_assets CASCADE;
               
               DROP TABLE IF EXISTS staged_assets CASCADE;
               DROP TABLE IF EXISTS staged_asset_categories CASCADE;
               DROP TABLE IF EXISTS staged_ratings CASCADE;
               DROP TABLE IF EXISTS staged_values CASCADE;
                ''')

# Creating the database structure
createdb = '''

CREATE TABLE SOURCES_MASTER(
    source_type VARCHAR(100),
    
    PRIMARY KEY(source_type)
    
    );

CREATE TABLE CATEGORIES_MASTER(
    category VARCHAR(200),
    
    PRIMARY KEY(category)
    
    );

CREATE TABLE COMMUNITIES_MASTER(
    community_geo_id INT,
    
    community_name VARCHAR(200),
    
    community_class_code CHAR(2),
    
    PRIMARY KEY(community_geo_id)
    
    );

CREATE TABLE VALUES_MASTER(
    value VARCHAR(200),
    
    PRIMARY KEY(value)
    );

CREATE TABLE ASSETS(
    asset_id CHAR(36) NOT NULL,
    asset_name VARCHAR(250) NOT NULL,
    asset_type VARCHAR(12) CHECK(asset_type IN ('Tangible', 'Intangible')),
    community_geo_id INT NOT NULL,
    source_type VARCHAR(100) NOT NULL,
    description TEXT,
    website TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    user_upload_ip TEXT,
    generated_timestamp TIMESTAMP,
    
    PRIMARY KEY (asset_id),
    
    CONSTRAINT fk_asset_community
        FOREIGN KEY(community_geo_id)
            REFERENCES communities_master(community_geo_id),
            
    CONSTRAINT fk_asset_source
        FOREIGN KEY(source_type)
            REFERENCES sources_master(source_type)
    );

CREATE TABLE ASSET_CATEGORIES(
    asset_id CHAR(36) NOT NULL,
    category VARCHAR(200) NOT NULL,
    
    PRIMARY KEY (asset_id, category),
    
    CONSTRAINT fk_assetcat_assetid
        FOREIGN KEY(asset_id)
            REFERENCES assets(asset_id),
            
    CONSTRAINT fk_assetcat_cat
        FOREIGN KEY(category)
            REFERENCES categories_master(category)
    
    );

CREATE TABLE RATINGS(
    rating_id CHAR(36) NOT NULL,
    asset_id CHAR(36) NOT NULL,
    user_community INT NOT NULL,
    user_upload_ip TEXT,
    generated_timestamp TIMESTAMP,
    rating_scale INT,
    comments TEXT,
    
    PRIMARY KEY(rating_id),
    
    CONSTRAINT fk_ratings_assetid
        FOREIGN KEY(asset_id)
            REFERENCES assets(asset_id),
            
    CONSTRAINT fk_ratings_community
        FOREIGN KEY(user_community)
            REFERENCES communities_master(community_geo_id)
    
    );

CREATE TABLE VALUES(
    rating_id CHAR(36) NOT NULL,
    value VARCHAR(200) NOT NULL,
    
    PRIMARY KEY(rating_id, value),
    
    CONSTRAINT fk_values_ratingid
        FOREIGN KEY(rating_id)
            REFERENCES ratings(rating_id),
            
    CONSTRAINT fk_values_value
        FOREIGN KEY(value)
            REFERENCES values_master(value)
    
    );

CREATE TABLE STAGED_ASSETS(
    staged_asset_id CHAR(36) NOT NULL,
    asset_name VARCHAR(250) NOT NULL,
    asset_type VARCHAR(12) CHECK(asset_type IN ('Tangible', 'Intangible')),
    community_geo_id INT NOT NULL,
    source_type VARCHAR(100) NOT NULL,
    description TEXT,
    website TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    user_name VARCHAR(200),
    user_role VARCHAR(300),
    user_upload_ip TEXT,
    generated_timestamp TIMESTAMP,
    
    PRIMARY KEY(staged_asset_id),
    
    CONSTRAINT fk_stagedasset_community
        FOREIGN KEY(community_geo_id)
            REFERENCES communities_master(community_geo_id),
            
    CONSTRAINT fk_stagedasset_source
        FOREIGN KEY(source_type)
            REFERENCES sources_master(source_type)
    );

CREATE TABLE STAGED_ASSET_CATEGORIES(
    staged_asset_id CHAR(36) NOT NULL,
    category VARCHAR(200) NOT NULL,
    
    PRIMARY KEY(staged_asset_id, category),
    
    CONSTRAINT fk_stagedassetcat_id
        FOREIGN KEY(staged_asset_id)
            REFERENCES staged_assets(staged_asset_id),
            
    CONSTRAINT fk_stagedassetcat_cat
        FOREIGN KEY(category)
            REFERENCES categories_master(category)
    
    );

CREATE TABLE STAGED_RATINGS(
    staged_rating_id CHAR(36) NOT NULL,
    staged_asset_id CHAR(36) NOT NULL,
    user_community INT NOT NULL,
    user_name VARCHAR(200),
    user_role VARCHAR(300),
    user_upload_ip TEXT,
    generated_timestamp TIMESTAMP,
    rating_scale INT,
    comments TEXT,
    
    PRIMARY KEY(staged_rating_id),
    
    CONSTRAINT fk_stagedratings_id
        FOREIGN KEY(staged_asset_id)
            REFERENCES staged_assets(staged_asset_id),
            
    CONSTRAINT fk_stagedratings_community
        FOREIGN KEY(user_community)
            REFERENCES communities_master(community_geo_id)
    
    );

CREATE TABLE STAGED_VALUES(
    staged_rating_id CHAR(36) NOT NULL,
    value VARCHAR(200) NOT NULL,
    
    PRIMARY KEY(staged_rating_id, value),
    
    CONSTRAINT fk_stagedvalues_rating
        FOREIGN KEY(staged_rating_id)
            REFERENCES staged_ratings(staged_rating_id),
            
    CONSTRAINT fk_stagedvalues_value
        FOREIGN KEY(value)
            REFERENCES values_master(value)
    
    );

CREATE TABLE MISSING_ASSETS(
    suggestion_id CHAR(36) NOT NULL,
    user_community INT NOT NULL,
    user_name VARCHAR(200),
    user_role VARCHAR(300),
    user_upload_ip TEXT,
    generated_timestamp TIMESTAMP,
    missing_asset_name VARCHAR(250),
    primary_category VARCHAR(200) NOT NULL,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    line LINE,
    polygon POLYGON,
    circle CIRCLE,
    
    PRIMARY KEY(suggestion_id),
    
    CONSTRAINT fk_missingasset_community
        FOREIGN KEY(user_community)
            REFERENCES communities_master(community_geo_id),
            
    CONSTRAINT fk_missingasset_cat
        FOREIGN KEY(primary_category)
            REFERENCES categories_master(category)
            
    );


'''

# Execute the query
cursor.execute(createdb)
conn.commit()
