from dotenv import load_dotenv
from connectors.spotify import SpotifyApiClient
import pandas as pd
import os
import requests
from assets.artist_id_list import extract_artist_id_list
from connectors.postgres import PostgreSqlClient
from sqlalchemy import Table, Column, MetaData, String,Integer,DateTime
from sqlalchemy.dialects import postgresql
import time


load_dotenv()

API_KEY_ID = os.environ.get("spotify_client_id")
API_SECRET_KEY = os.environ.get("spotify_client_secret")

def artist_id_list(tracks=list) -> list:
    artist_id_list = set() #using a set for deduplication
    for track in range(0,len(tracks)):
        artist_id_list.add(tracks[track]['artists'][0]['id']) # type: ignore

    return list(artist_id_list)



def get_artists(SpotifyApiClient =SpotifyApiClient,artist_ids=pd.DataFrame) -> dict:
    """This function gets data about artists, 50 at a time. stores the data points as
    a string of dictionary"""
    
    #construct the header to pass in the access token
    header={"Authorization": f"{SpotifyApiClient.token_type} {SpotifyApiClient.access_token}"}

    #get list of artists
    artist_list=artist_ids['artist_id'].tolist()

    dict_list=[]

    extract_time=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

    #pass 50 ids at a time
    for i in range(0,len(artist_list),50):

        #get sub_list of 50 ids
        sub_list=artist_list[i:i+50]
        ids=','.join(sub_list)

        
        response_json=requests.get(f"{SpotifyApiClient.base_url}/artists/?ids={ids}",headers=header).json()

        #loop through the response_json and form a dictionary for each artist
        for y in range (0,len(sub_list)):

            artist_dict = {'artist_id': response_json['artists'][y]['id'],
                        'artist': response_json['artists'][y]['name'],
                        'genres': response_json['artists'][y]['genres'],
                        'popularity': response_json['artists'][y]['popularity'],
                        'total_followers':response_json['artists'][y]['followers']['total'],
                        'last_modified': extract_time       
            }
            dict_list.append(artist_dict)

    return dict_list


def load_artist(PostgresSqlClient: PostgreSqlClient, list:list):
    metadata=MetaData()

    #construct the metadata
    artist_table=Table('artist',metadata,
                          Column('artist_id',String,primary_key=True),
                          Column('artist',String),
                          Column('genres',String),
                          Column('popularity',Integer),
                          Column('total_followers',Integer),
                          Column('last_modified',DateTime)
    )

    #creates the table if does not exist
    metadata.create_all(PostgresSqlClient.engine)

    #have to create the insert statement first to then create upsert statement
    insert_statement=postgresql.insert(artist_table).values(list)
    
    upsert_statement =insert_statement.on_conflict_do_update(
        index_elements=['artist_id'],
        #for each column not part of the conflict key, update it to the new value
        set_={c.key: c for c in insert_statement.excluded if c.key not in ['artist_id']}) 
    
    PostgresSqlClient.engine.execute(upsert_statement)

    print('uploaded to database')



### tests
# spotify_client=SpotifyApiClient(API_KEY_ID,API_SECRET_KEY)


# file_path="data/artist_ids.csv"
# artist_list=extract_artist_id_list(file_path=file_path)



# dict_list=get_artists(SpotifyApiClient=spotify_client, artist_ids=artist_list)
# load_artist(PostgresSqlClient=PostgreSqlClient, list=dict_list)