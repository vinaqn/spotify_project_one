from dotenv import load_dotenv
from connectors.spotify import SpotifyApiClient
import pandas as pd
import os
import requests
from assets.track import get_tracks
from assets.extract_ids import extract_track_id_list
from connectors.postgres import PostgreSqlClient 
from sqlalchemy import Table, MetaData,Column, Integer, DateTime, String
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import ARRAY

#Sabrina Carpenter album: 1aqg30bNvLSWgShZgX4oop


#to be ran after track.py to get album data
def get_albums(SpotifyApiClient=SpotifyApiClient,album_ids=list) -> list:
    """This function gets album information based on the list of album ids passed in"""
    #first run get_tracks to compile a list of tracks with album data
    #extract the album ids from the track data - album_id_list method
    #loop through the album ids 20 at a time(max limit for spotify API)
    #store the 20 albums in a new list
    #use the list of 20 albums to call the spotify API
    #append the results to a master list

    header={"Authorization": f"{SpotifyApiClient.token_type} {SpotifyApiClient.access_token}"}

    main_list = []

    for i in range(0, len(album_ids), 20):
        sub_list = album_ids[i:i+20]
        ids = ','.join(sub_list)
        response_json=requests.get(f"{SpotifyApiClient.base_url}/albums?ids={ids}",headers=header).json()
        main_list.extend(response_json['albums'])

    return main_list

def album_id_list(tracks=list) -> list:
    album_id_list = set() #using a set for deduplication
    for track in range(0,len(tracks)):
        album_id_list.add(tracks[track]['album']['uri'][14:]) # type: ignore

    return list(album_id_list)

#to be ran last, should give us the structured album data
def get_album_dict(albums_list=list) -> list:
    album_dict = {}
    album_dict_list = []

    for i in range(0,len(albums_list)):        
        album_dict = {
            'album_id' : albums_list[i]['id'],
            'album_name' : albums_list[i]['name'], # type: ignore
            'album_type' : albums_list[i]['album_type'], # type: ignore
            'artist_id' : albums_list[i]['artists'][0]['id'], # type: ignore
            'album_release_date' : albums_list[i]['release_date'], # type: ignore
            'release_date_precision' : albums_list[i]['release_date_precision'], # type: ignore
            'total_tracks' : albums_list[i]['tracks']['total'], # type: ignore
            'track_list' : albums_list[i]['tracks']['items'][0]['name'], # type: ignore
            'label' : albums_list[i]['label'], # type: ignore
            'popularity' : albums_list[i]['popularity'], # type: ignore
            'markets' : albums_list[i]['available_markets'] # type: ignore
        }

        if len(albums_list[i]['tracks']['items']) > 1: # type: ignore
            for j in range(1,len(albums_list[i]['tracks']['items'])): # type: ignore
                album_dict['track_list'] = album_dict['track_list'] + ", " + albums_list[i]['tracks']['items'][j]['name'] # type: ignore

        album_dict_list.append(album_dict)

    return album_dict_list


def load_album(PostgreSqlClient=PostgreSqlClient, list=list):
    metadata=MetaData()

    #construct the metadata
    album_table=Table('album',metadata,
                          Column('album_id',String,primary_key=True),
                          Column('album_name',String),
                          Column('album_type',String),
                          Column('artist_id',String),
                          Column('album_release_date',String),
                          Column('release_date_precision',String),
                          Column('total_tracks',Integer),
                          Column('track_list',String),
                          Column('label',String),
                          Column('popularity',Integer),
                          Column('markets',ARRAY(String))
    )

    #creates the table if does not exist
    metadata.create_all(PostgreSqlClient.engine)

    with PostgreSqlClient.engine.begin() as conn: # opens a trasaction
        #have to create the insert statement first to then create upsert statement

        for i in range(0,len(list),1000):   
            sub_list = list[i:i+1000]
            insert_statement=postgresql.insert(album_table).values(sub_list)
            
            upsert_statement =insert_statement.on_conflict_do_update(
                index_elements=['album_id'],
                #for each column not part of the conflict key, update it to the new value
                set_={c.key: c for c in insert_statement.excluded if c.key not in ['album_id']}) 
            
            try:
                conn.execute(upsert_statement)
                print(f"Inserted {i}-{min(i+1000, len(list))}")
            except Exception as e:
                print(f"❌ Error at chunk {i}-{min(i+1000, len(list))}: {e}")

    print('uploaded to database')

    return


#tests ----------------------------------------------

# load_dotenv()

# API_KEY_ID = os.environ.get("spotify_client_id")
# API_SECRET_KEY = os.environ.get("spotify_client_secret")


# #database details
# DB_SERVER_NAME= os.environ.get("DB_SERVER_NAME")
# DB_DATABASE_NAME = os.environ.get("DB_DATABASE_NAME")
# DB_USERNAME = os.environ.get("DB_USERNAME")
# DB_PASSWORD = os.environ.get("DB_PASSWORD")
# DB_PORT = os.environ.get("DB_PORT")




# spotify_client=SpotifyApiClient(API_KEY_ID,API_SECRET_KEY)

# postgres_client=PostgreSqlClient(db_server_name=DB_SERVER_NAME,
#                                 db_database_name=DB_DATABASE_NAME,
#                                 db_username=DB_USERNAME,
#                                 db_password=DB_PASSWORD,
#                                 db_port=DB_PORT)

# #tracks_id5000 is a small sample of track_ids for testing purposes(saves time)
# file_path="data/track_ids5000.csv"
# #returns a dataframe of the raw data from the preloaded CSV, not the API
# track_list=extract_track_id_list(file_path=file_path)

# #returns a list of raw data in a list, include album ids found in [index]['album']['uri']
# print("getting tracks and album ids")
# tester = get_tracks(SpotifyApiClient=spotify_client,track_ids=track_list) 
# #retruns a list of only the album ids

# print("extracting album ids")
# album_ids = album_id_list(tester)

# print("passing in album ids to get album info")
# album_info = get_albums(SpotifyApiClient=spotify_client,album_ids=album_ids)

# album_dict_result = get_album_dict(album_info)

# print("loading in album data into database")
# load_album(PostgreSqlClient=postgres_client,list=album_dict_result) 
