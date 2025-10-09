import pandas as pd

def extract_track_id_list(file_path: str) ->pd.DataFrame:
    """Extracts a list of track ids"""
    df = pd.read_csv(file_path)

    return df

def extract_artist_id_list_from_track_ids(file_path: str) ->pd.DataFrame:
    """Extracts a list of artist ids from the track ids file"""
    df = pd.read_csv(file_path)

    df.drop(columns=['track_name','track_id','album_name','album_id','album_type','markets'],inplace=True)

    #extract only the artist ids from the track ids file
    artist_ids = df.drop_duplicates(subset='artist_id').reset_index(drop=True)

    return artist_ids