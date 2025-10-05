from dotenv import load_dotenv
from connectors.spotify import SpotifyApiClient
from connectors.postgres import PosgreSqlClient
import os

load_dotenv()

API_KEY_ID = os.environ.get("spotify_client_id")
API_SECRET_KEY = os.environ.get("spotify_client_secret")


#database details
SERVER_NAME= os.environ.get("SERVER_NAME")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
PORT = os.environ.get("PORT")






spotify_client=SpotifyApiClient(API_KEY_ID,API_SECRET_KEY)

postgres_client=PosgreSqlClient(server_name=SERVER_NAME,
                                database_name=DATABASE_NAME,
                                username=USERNAME,
                                password=PASSWORD,
                                port=PORT)


# TESTING PUSH -Thomas
# TEST PUSH 2 -Thomas