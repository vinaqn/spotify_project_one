from dotenv import load_dotenv
from connectors.spotify import SpotifyApiClient
import pandas as pd
import os
import requests
from assets.artist_id_list import extract_artist_id_list
from connectors.postgres import PostgreSqlClient
from sqlalchemy import Table, Column, MetaData, String,Integer
from sqlalchemy.dialects import postgresql


load_dotenv()

API_KEY_ID = os.environ.get("spotify_client_id")
API_SECRET_KEY = os.environ.get("spotify_client_secret")



def get_artist(SpotifyApiClient =SpotifyApiClient,artist_id=str) -> pd.DataFrame:
    """This function gets data about one artist based on the artist_id passed in"""
    
    #construct the header to pass in the access token
    header={"Authorization": f"{SpotifyApiClient.token_type} {SpotifyApiClient.access_token}"}
    
    
    response_json=requests.get(f"{SpotifyApiClient.base_url}/artists/{artist_id}",headers=header).json()

    artist_dict = {'artist_id': response_json['id'],
                   'artist': response_json['name'],
                   'genres': response_json['genres'],
                   'popularity': response_json['popularity'],
                   'total_followers':response_json['followers']['total']       
    }
    return artist_dict

def construct_artist_data_dict(artist_ids=pd.DataFrame, SpotifyApiClient=SpotifyApiClient) ->list:
    """this function constructs a list of artist dictionaries"""

    dict_list=[]

    #loops through the list of artist ids
    for index,row in artist_ids.iterrows():
        
        #get artist info from API
        dict=get_artist(SpotifyApiClient=SpotifyApiClient,artist_id=row['artist_id'])

        #append artist info into a list
        dict_list.append(dict)

    return dict_list

def load_artist(PostgresSqlClient: PostgreSqlClient, list:list):
    metadata=MetaData()

    #construct the metadata
    artist_table=Table('artist',metadata,
                          Column('artist_id',String,primary_key=True),
                          Column('artist',String),
                          Column('genres',String),
                          Column('popularity',Integer),
                          Column('total_followers',Integer)
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
spotify_client=SpotifyApiClient(API_KEY_ID,API_SECRET_KEY)


file_path="data/artist_ids.csv"
artist_list=extract_artist_id_list(file_path=file_path)

# dict_list=construct_artist_data_dict(artist_ids=artist_list,SpotifyApiClient=spotify_client)
# load_artist(PostgresSqlClient=PostgreSqlClient, list=dict_list)