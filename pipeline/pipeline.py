from dotenv import load_dotenv
from connectors.spotify import SpotifyApiClient
from connectors.postgres import PostgreSqlClient
from assets.artist import get_artists, load_artist, artist_id_list
from assets.track import get_tracks, track_id_dict, load_tracks, load_track_ids
from assets.categories import get_categories, load_categories
from assets.extract_ids import extract_track_id_list, extract_artist_id_list_from_track_ids
from assets.album import get_albums, get_album_dict, load_album, album_id_list
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

#load track_ids
pipeline_logger.logger.info(f"Loading track ids into database")
file_path="data/test_track_ids100.csv"
track_ids = extract_track_id_list(file_path=file_path)
load_track_ids(PostgreSqlClient=postgres_client, track_ids=track_ids)

#extracting tracks
pipeline_logger.logger.info(f"Extracting track_ids")
track_ids = extract_track_id_list(file_path=file_path)
raw_track_list = get_tracks(SpotifyApiClient=spotify_client, track_ids=track_ids)
track_dict_result = track_id_dict(raw_track_list)

#loading tracks
load_tracks(PostgreSqlClient=postgres_client, track_list=track_dict_result)

#extracting and loading artist_ids
pipeline_logger.logger.info(f"Extracting artist_ids")

#extract and load in artist info
pipeline_logger.logger.info(f"Extracting artist info")
artist_id_list=artist_id_list(raw_track_list)
artist_dict_list=get_artists(SpotifyApiClient=spotify_client, artist_list=artist_id_list)

pipeline_logger.logger.info(f"Loading artist info into database")
load_artist(PostgresSqlClient=postgres_client, list=artist_dict_list)

#extracting and loading categories
pipeline_logger.logger.info(f"Extracting categories")
categories = get_categories(SpotifyApiClient=spotify_client)

pipeline_logger.logger.info(f"Loading categories info")
load_categories(PostgresSqlClient=postgres_client,list=categories)

#extracting and loading albums
pipeline_logger.logger.info(f"Extracting album info")
album_ids = album_id_list(raw_track_list)
album_info = get_albums(SpotifyApiClient=spotify_client,album_ids=album_ids)
album_dict_result = get_album_dict(album_info)

pipeline_logger.logger.info(f"Loading album info")
load_album(PostgreSqlClient=postgres_client,list=album_dict_result) 


