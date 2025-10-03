import pandas as pd

def extract_artist_id_list(file_path: str) ->pd.DataFrame:
    """Extracts a list of artists and their Spotify ids and read as a panda data frame"""
    df =pd.read_csv(file_path)

    return df


file_path="data/artist_ids.csv"

print(extract_artist_id_list(file_path=file_path))