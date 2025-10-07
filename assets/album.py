from dotenv import load_dotenv
from connectors.spotify import SpotifyApiClient
import pandas as pd
import os
import requests
from assets.track import get_tracks
from assets.track_id_list import extract_track_id_list

#Sabrina Carpenter album: 1aqg30bNvLSWgShZgX4oop

load_dotenv()

API_KEY_ID = os.environ.get("spotify_client_id")
API_SECRET_KEY = os.environ.get("spotify_client_secret")

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
    album_id_list = []
    for track in range(0,len(tracks)):
        album_id_list.append(tracks[track]['album']['uri'][14:]) # type: ignore

    return album_id_list

#to be ran last, should give us the structured album data
def get_album_dict(albums_list=list) -> list:
    album_dict = {}
    album_dict_list = []

    for i in range(0,len(albums_list)):        
        album_dict = {
            'album_name' : albums_list[i]['name'],
            'album_id' : albums_list[i]['id'],
            'album_type' : albums_list[i]['album_type'],
            'artist_name' : albums_list[i]['artists'][0]['name'],
            'album_release_date' : albums_list[i]['release_date'],
            'total_tracks' : albums_list[i]['tracks']['total'],
            'track_list' : albums_list[i]['tracks']['items'][0]['name'],
            'label' : albums_list[i]['label'],
            'popularity' : albums_list[i]['popularity'],
            'markets' : albums_list[i]['available_markets']
        }

        if len(albums_list[i]['tracks']['items']) > 1:
            for j in range(1,len(albums_list[i]['tracks']['items'])):
                album_dict['track_list'] = album_dict['track_list'] + ", " + albums_list[i]['tracks']['items'][j]['name']

        album_dict_list.append(album_dict)

    return album_dict_list

#tests ----------------------------------------------

spotify_client=SpotifyApiClient(API_KEY_ID,API_SECRET_KEY)

#tracks_id5000 is a small sample of track_ids for testing purposes(saves time)
file_path="data/track_ids100.csv"
#returns a dataframe of the raw data from the preloaded CSV, not the API
track_list=extract_track_id_list(file_path=file_path)

#returns a list of raw data in a list, include album ids found in [index]['album']['uri']
tester = get_tracks(SpotifyApiClient=spotify_client,track_ids=track_list) 
#retruns a list of only the album ids
album_ids = album_id_list(tester)
#print("hello world")
#print(album_ids[0])
album_info = get_albums(SpotifyApiClient=spotify_client,album_ids=album_ids)
#print(album_info[1])
df = pd.DataFrame(album_info)
# print (album_info[3])
#print (df.iloc[3])

album_dict_result = get_album_dict(album_info)
df2 = pd.DataFrame(album_dict_result)
print (df2[['album_name','arist_name','total_tracks','track_list']])
#print (album_dict_result[0])