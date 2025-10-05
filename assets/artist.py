from dotenv import load_dotenv
from connectors.spotify import SpotifyApiClient
import pandas as pd
import os
import requests
from assets.artist_id_list import extract_artist_id_list



load_dotenv()

API_KEY_ID = os.environ.get("spotify_client_id")
API_SECRET_KEY = os.environ.get("spotify_client_secret")



def get_artist(SpotifyApiClient =SpotifyApiClient,artist_id=str) -> pd.DataFrame:
    """This function gets data about one artist based on the artist_id passed in"""
    
    #construct the header to pass in the access token
    header={"Authorization": f"{SpotifyApiClient.token_type} {SpotifyApiClient.access_token}"}
    
    
    response_json=requests.get(f"{SpotifyApiClient.base_url}/artists/{artist_id}",headers=header).json()

    artist_dict = {'id': response_json['id'],
                   'name': response_json['name'],
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



### tests
spotify_client=SpotifyApiClient(API_KEY_ID,API_SECRET_KEY)


file_path="data/artist_ids.csv"
artist_list=extract_artist_id_list(file_path=file_path)

construct_artist_data_dict(artist_ids=artist_list,SpotifyApiClient=spotify_client)