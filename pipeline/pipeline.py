from dotenv import load_dotenv
from connectors.spotify import SpotifyApiClient
import os

load_dotenv()

API_KEY_ID = os.environ.get("spotify_client_id")
API_SECRET_KEY = os.environ.get("spotify_client_secret")


spotify_client=SpotifyApiClient(API_KEY_ID,API_SECRET_KEY)

spotify_client.get_artist("7GlBOeep6PqTfFi59PTUUN")

# TESTING PUSH -Thomas
# TEST PUSH 2 -Thomas