from dotenv import load_dotenv
from connectors.spotify import SpotifyApiClient
from connectors.postgres import PostgreSqlClient
from assets.artist_id_list import extract_artist_id_list,load_artist_id_list
from assets.artist import construct_artist_data_dict, load_artist
import os

load_dotenv()

API_KEY_ID = os.environ.get("spotify_client_id")
API_SECRET_KEY = os.environ.get("spotify_client_secret")


#database details
DB_SERVER_NAME= os.environ.get("DB_SERVER_NAME")
DB_DATABASE_NAME = os.environ.get("DB_DATABASE_NAME")
DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_PORT = os.environ.get("DB_PORT")






spotify_client=SpotifyApiClient(API_KEY_ID,API_SECRET_KEY)

postgres_client=PostgreSqlClient(db_server_name=DB_SERVER_NAME,
                                db_database_name=DB_DATABASE_NAME,
                                db_username=DB_USERNAME,
                                db_password=DB_PASSWORD,
                                db_port=DB_PORT)


#test extracting and loading artist_ids
artist_id_df=extract_artist_id_list("data/artist_ids.csv")
load_artist_id_list(PostgresSqlClient=postgres_client,df=artist_id_df)

load_artist_id_list(PostgresSqlClient=postgres_client,df=artist_id_df)

#extract and load in artist info
artist_list=construct_artist_data_dict(artist_ids=artist_id_df,SpotifyApiClient=spotify_client)

load_artist(PostgresSqlClient=postgres_client,list=artist_list)


# TESTING PUSH -Thomas
# TEST PUSH 2 -Thomas