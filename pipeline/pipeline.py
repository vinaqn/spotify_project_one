from dotenv import load_dotenv
from connectors.spotify import SpotifyApiClient
from connectors.postgres import PostgreSqlClient
from assets.artist_id_list import extract_artist_id_list,load_artist_id_list
from assets.artist import get_artists, load_artist
from assets.pipeline_logger import PipelineLogger
import os

pipeline_logger=PipelineLogger("spotify_project","logs")


pipeline_logger.logger.info(f"Starting {pipeline_logger.pipeline_name}")


pipeline_logger.logger.info(f"Loading environment variables")

load_dotenv()

API_KEY_ID = os.environ.get("spotify_client_id")
API_SECRET_KEY = os.environ.get("spotify_client_secret")


#database details
DB_SERVER_NAME= os.environ.get("DB_SERVER_NAME")
DB_DATABASE_NAME = os.environ.get("DB_DATABASE_NAME")
DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_PORT = os.environ.get("DB_PORT")




#instantiate Spotify API Client
pipeline_logger.logger.info(f"Creating Spotify API client")
spotify_client=SpotifyApiClient(API_KEY_ID,API_SECRET_KEY)

#instantiate PostgreSQL client
pipeline_logger.logger.info(f"Creating PostgreSQL client")
postgres_client=PostgreSqlClient(db_server_name=DB_SERVER_NAME,
                                db_database_name=DB_DATABASE_NAME,
                                db_username=DB_USERNAME,
                                db_password=DB_PASSWORD,
                                db_port=DB_PORT)


#extracting and loading artist_ids
pipeline_logger.logger.info(f"Extracting artist_ids")


#extract and load in artist info
pipeline_logger.logger.info(f"Extracting artist info")
artist_id_df=extract_artist_id_list("data/artist_ids.csv")
artist_dict_list=get_artists(SpotifyApiClient=spotify_client, artist_ids=artist_id_df)

pipeline_logger.logger.info(f"Loading artist info into database")
load_artist(PostgresSqlClient=postgres_client, list=artist_dict_list)


# TESTING PUSH -Thomas
# TEST PUSH 2 -Thomas