from dotenv import load_dotenv
from connectors.spotify import SpotifyApiClient
import pandas as pd
import os
import requests
from assets.track_id_list import extract_track_id_list
from connectors.postgres import PostgreSqlClient
from sqlalchemy import Table, Column, MetaData, String
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import ARRAY


def get_tracks(SpotifyApiClient=SpotifyApiClient,track_ids=pd.DataFrame) -> pd.DataFrame:
    """This function gets all the tracks available on spotify"""
    #construct the header to pass in the access token
    header={"Authorization": f"{SpotifyApiClient.token_type} {SpotifyApiClient.access_token}"}
    
    #load the csv of track ids into a dataframe - track_ids contains the huge list of tracks ids
    #convert the track ids column into a list 
    #loop through the list of track ids 50 at a time(max limit for spotify API)
    #store the 50 tracks in a new list
    #use the list of 50 tracks to call the spotify API
    #append the results to a master list
    #convert the master list into a dataframe and return it

    track_list = track_ids["track_id"].tolist()
    main_list = []

    for i in range(0, len(track_list), 50):
        #starting from i get the next 50 ids in the list
        sub_list = track_list[i:i+50]
        #joins the list contents into a string separated by commas
        ids = ','.join(sub_list)
        #make the API call with the list of 50 ids
        response_json=requests.get(f"{SpotifyApiClient.base_url}/tracks?ids={ids}",headers=header).json()

        #append the response to the main_list of tracks
        main_list.extend(response_json['tracks'])

    return main_list

def track_id_dict(tracks=list) -> list:
    track_dict = {}
    track_dict_list = []

    for i in range(0,len(tracks)):        
        track_dict = {
            'track_name' : tracks[i]['name'], # type: ignore
            'track_id' : tracks[i]['id'],
            'album_name' : tracks[i]['album']['name'], # type: ignore
            'album_id' : tracks[i]['album']['uri'][14:], # type: ignore
            'album_type' : tracks[i]['album']['album_type'], # type: ignore
            'artist_name' : tracks[i]['album']['artists'][0]['name'], # type: ignore
            'artist_id' : tracks[i]['album']['artists'][0]['id'], # type: ignore
            'markets' : tracks[i]['album']['available_markets'] # type: ignore
        }

        track_dict_list.append(track_dict)

    return track_dict_list

def load_tracks(PostgreSqlClient=PostgreSqlClient, track_list=list):
    metadata=MetaData()

    #metadata
    track_table=Table('tracks',metadata,
                          Column('track_id',String,primary_key=True),
                          Column('track_name',String),
                          Column('album_name',String),
                          Column('album_id',String),
                          Column('album_type',String),
                          Column('artist_name',String),
                          Column('artist_id',String),
                          Column('markets',ARRAY(String))
    )

    metadata.create_all(PostgreSqlClient.engine)


    with PostgreSqlClient.engine.begin() as conn: # opens a trasaction

        for i in range(0,len(track_list),1000):   
            sub_list = track_list[i:i+1000]

            insert_statement=postgresql.insert(track_table).values(sub_list)
            
            upsert_statement=insert_statement.on_conflict_do_update(
                index_elements=['track_id'],
                #for each column not part of the conflict key, update it to the new value
                set_={c.key: c for c in insert_statement.excluded if c.key not in ['track_id']}) 
            

            try:
                conn.execute(upsert_statement)
                print(f"Inserted {i}-{min(i+1000, len(track_list))}")
            except Exception as e:
                print(f"❌ Error at chunk {i}-{min(i+1000, len(track_list))}: {e}")
            
    
    

    print('uploaded to database')

    return

def load_track_ids(PostgreSqlClient=PostgreSqlClient, track_ids=pd.DataFrame):
    metadata=MetaData()

    #metadata
    track_id_table=Table('track_id_list',metadata,
                          Column('track_id',String,primary_key=True)    )

    metadata.create_all(PostgreSqlClient.engine)

    insert_statement=postgresql.insert(track_id_table).values(track_ids.to_dict(orient='records'))
    
    upsert_statement=insert_statement.on_conflict_do_nothing(
        index_elements=['track_id']) 

    
    PostgreSqlClient.engine.execute(upsert_statement)

    print('uploaded to database')

    return

# #tests --------

# load_dotenv()


# API_KEY_ID = os.environ.get("spotify_client_id")
# API_SECRET_KEY = os.environ.get("spotify_client_secret")

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
# file_path="data/track_ids100.csv"
# track_list=extract_track_id_list(file_path=file_path)
# raw_track_table = get_tracks(SpotifyApiClient=spotify_client,track_ids=track_list)
# track_dict_result = track_id_dict(raw_track_table)



# #load_tracks(PostgreSqlClient=postgres_client, track_list=track_dict_result)

# load_track_ids(PostgreSqlClient=postgres_client, track_ids=track_list)