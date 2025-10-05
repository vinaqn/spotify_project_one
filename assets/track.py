from dotenv import load_dotenv
from connectors.spotify import SpotifyApiClient
import pandas as pd
import os
import requests
from assets.track_id_list import extract_track_id_list

load_dotenv()

API_KEY_ID = os.environ.get("spotify_client_id")
API_SECRET_KEY = os.environ.get("spotify_client_secret")

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

    #print (pd.DataFrame(main_list).head())
    #print(main_list[0])
    return main_list

# #tests
# spotify_client=SpotifyApiClient(API_KEY_ID,API_SECRET_KEY)

# #tracks_id5000 is a small sample of track_ids for testing purposes(saves time)
# file_path="data/track_ids5000.csv"
# track_list=extract_track_id_list(file_path=file_path)

# tester = get_tracks(SpotifyApiClient=spotify_client,track_ids=track_list)
# print (tester[0]['album']['uri'])
# print("hello world")
# #tester.to_csv("tester.csv",index=False)