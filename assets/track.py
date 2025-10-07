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
<<<<<<< HEAD
        
=======
>>>>>>> a6b03a3fff5a2ed64903d171bd0882ec93868359
        # print ("hello world")
        # print (response_json)
        #append the response to the main_list of tracks
        main_list.extend(response_json['tracks'])

    #print (main_list[10])
    # print (main_list[10]['album']['artists'][0]['name'])
    # print (main_list[10]['album']['name'])
    return main_list

def track_id_dict(tracks=list) -> list:
    track_dict = {}
    track_dict_list = []

    for i in range(0,len(tracks)):        
        track_dict = {
            'track_name' : tracks[i]['name'],
            'track_id' : tracks[i]['id'],
            'album_name' : tracks[i]['album']['name'],
            'album_id' : tracks[i]['album']['uri'][14:],
            'album_type' : tracks[i]['album']['album_type'],
<<<<<<< HEAD
            'artist_name' : tracks[i]['album']['artists'][0]['name'],
            'artist_id' : tracks[i]['album']['artists'][0]['id'],
=======
            'arist_name' : tracks[i]['album']['artists'][0]['name'],
>>>>>>> a6b03a3fff5a2ed64903d171bd0882ec93868359
            'markets' : tracks[i]['album']['available_markets']
        }

        track_dict_list.append(track_dict)

    return track_dict_list


#tests
spotify_client=SpotifyApiClient(API_KEY_ID,API_SECRET_KEY)

#tracks_id5000 is a small sample of track_ids for testing purposes(saves time)
file_path="data/track_ids100.csv"
track_list=extract_track_id_list(file_path=file_path)

tester = get_tracks(SpotifyApiClient=spotify_client,track_ids=track_list)
track_dict_result = track_id_dict(tester)
df = pd.DataFrame(track_dict_result)
<<<<<<< HEAD
print (df[['artist_name','artist_id']])
df.to_csv("full_artist_ids.csv",index=False)
=======
#print (df[['album_name','track_name']])
>>>>>>> a6b03a3fff5a2ed64903d171bd0882ec93868359
#print (track_dict_result[0:10])

# print (tester[0]['album']['uri'])
# print("hello world")
# print(tester[0])
#tester.to_csv("tester.csv",index=False)