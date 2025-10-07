import pandas as pd

def extract_track_id_list(file_path: str) ->pd.DataFrame:
    """Extracts a list of track ids"""
    df =pd.read_csv(file_path)

    return df