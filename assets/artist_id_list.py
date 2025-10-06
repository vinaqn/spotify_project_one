import pandas as pd
import connectors.postgres as PostgresSqlClient
from sqlalchemy import Table, Column, Integer, String, MetaData, Float
from sqlalchemy.dialects import postgresql

def extract_artist_id_list(file_path: str) ->pd.DataFrame:
    """Extracts a list of artists and their Spotify ids and read as a panda data frame"""
    df =pd.read_csv(file_path,encoding='UTF-8',sep=',')

    return df

def load_artist_id_list(PostgresSqlClient: PostgresSqlClient, df:pd.DataFrame):
    metadata=MetaData()

    #construct the metadata
    artist_id_table=Table('artist_ids_list',metadata,
                          Column('artist_id',String,primary_key=True),
                          Column('artist_name',String)
    )

    #creates the table if does not exist
    metadata.create_all(PostgresSqlClient.engine)

    #have to create the insert statement first to then create upsert statement
    insert_statement=postgresql.insert(artist_id_table).values(df.to_dict(orient='records'))
    
    upsert_statement =insert_statement.on_conflict_do_update(
        index_elements=['artist_id'],
        #for each column not part of the conflict key, update it to the new value
        set_={c.key: c for c in insert_statement.excluded if c.key not in ['id']}) 
    
    PostgresSqlClient.engine.execute(upsert_statement)

    print('uploaded to database')
    

    return










# test
# file_path="data/artist_ids.csv"
# print(extract_artist_id_list(file_path=file_path))