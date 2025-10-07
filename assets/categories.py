from dotenv import load_dotenv
from connectors.spotify import SpotifyApiClient
import os
import requests
from connectors.postgres import PostgreSqlClient
from sqlalchemy import Table, MetaData,Column,String, Integer,DateTime
from sqlalchemy.dialects import postgresql


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

    #loop through json and create dict of needed info
    for i in range(0,len(categories_raw3)):
        category_dict={'category_id':categories_raw3[i]['id'],
                       'category':categories_raw3[i]['name']
        }
        categories.append(category_dict)

    return categories

def load_categories(PostgresSqlClient: PostgreSqlClient, list:list):
    metadata=MetaData()

    #construct the metadata
    categories_table=Table('category',metadata,
                          Column('category_id',String,primary_key=True),
                          Column('category',String)
    )

    #creates the table if does not exist
    metadata.create_all(PostgresSqlClient.engine)

    #have to create the insert statement first to then create upsert statement
    insert_statement=postgresql.insert(categories_table).values(list)
    
    upsert_statement =insert_statement.on_conflict_do_update(
        index_elements=['category_id'],
        #for each column not part of the conflict key, update it to the new value
        set_={c.key: c for c in insert_statement.excluded if c.key not in ['category_id']}) 
    
    PostgresSqlClient.engine.execute(upsert_statement)

    print('uploaded to database')


#tests 
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



categories = get_categories(SpotifyApiClient=spotify_client)

load_categories(PostgresSqlClient=postgres_client,list=categories)