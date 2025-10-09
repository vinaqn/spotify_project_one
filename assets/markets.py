from dotenv import load_dotenv
from connectors.spotify import SpotifyApiClient
import os
import requests
load_dotenv()

API_KEY_ID = os.environ.get("spotify_client_id")
API_SECRET_KEY = os.environ.get("spotify_client_secret")

def get_markets(SpotifyApiClient=SpotifyApiClient) -> list:
    """This function returns all the markets that spotify is available in"""

    header={"Authorization": f"{SpotifyApiClient.token_type} {SpotifyApiClient.access_token}"}

    response_json=requests.get(f"{SpotifyApiClient.base_url}/markets",headers=header).json()

    markets = response_json
    return markets


#tests 
spotify_client=SpotifyApiClient(API_KEY_ID,API_SECRET_KEY)

markets = get_markets(SpotifyApiClient=spotify_client)
print (markets)