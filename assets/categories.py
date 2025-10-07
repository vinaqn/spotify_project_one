from dotenv import load_dotenv
from connectors.spotify import SpotifyApiClient
import os
import requests
load_dotenv()

API_KEY_ID = os.environ.get("spotify_client_id")
API_SECRET_KEY = os.environ.get("spotify_client_secret")

<<<<<<< HEAD
=======
#to be ran after track.py to get album data
>>>>>>> a6b03a3fff5a2ed64903d171bd0882ec93868359
def get_categories(SpotifyApiClient=SpotifyApiClient) -> list:
    """This function returns all the categories that spotify has"""

    header={"Authorization": f"{SpotifyApiClient.token_type} {SpotifyApiClient.access_token}"}

    response_json=requests.get(f"{SpotifyApiClient.base_url}/browse/categories?limit=50",headers=header).json()
    categories_raw1 = response_json['categories']['items']
    #now request the rest of the categories with offset and combine the two lists
    response_json2=requests.get(f"{SpotifyApiClient.base_url}/browse/categories?limit=50&offset=50",headers=header).json()
    categories_raw2 = response_json2['categories']['items']

    #combine the two lists of categories, the data is still raw, it includes a lot of unneeded information
    categories_raw3 = categories_raw1 + categories_raw2

    categories = []

    for i in range(0,len(categories_raw3)):
        categories.append(categories_raw3[i]['name'])

    return categories


#tests 
spotify_client=SpotifyApiClient(API_KEY_ID,API_SECRET_KEY)

categories = get_categories(SpotifyApiClient=spotify_client)
print (categories)