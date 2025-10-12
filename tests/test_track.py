import pytest

from assets.track import track_id_dict

"""
def track_id_dict(tracks=list) -> list:
    track_dict = {}
    track_dict_list = []

    for i in range(0,len(tracks)):        
        track_dict = {
            'track_name' : tracks[i]['name'], # type: ignore
            'track_id' : tracks[i]['id'],
            'album_name' : tracks[i]['album']['name'], # type: ignore
            'album_id' : tracks[i]['album']['uri'][14:], # type: ignore
            'album_type' : tracks[i]['album']['album_type'], # type: ignore
            'artist_name' : tracks[i]['album']['artists'][0]['name'], # type: ignore
            'artist_id' : tracks[i]['album']['artists'][0]['id'], # type: ignore
            'markets' : tracks[i]['album']['available_markets'], # type: ignore
            'duration_ms' : tracks[i]['duration_ms'], # type: ignore
            'popularity' : tracks[i]['popularity']# type: ignore
        }

        track_dict_list.append(track_dict)

    return track_dict_list

"""


def make_sample_track(index: int, markets=None):
#returns a sample track dictionary with the same structure as the Spotify API response
    if markets is None:
        markets = ["US", "GB", "FR"]

    return {
        "name": f"track-{index}",
        "id": f"id-{index}",
        "duration_ms": index + 100,
        "popularity": index + 50,
        "album": {
            "name": f"album-{index}",
            #spotify album uri often looks like "spotify:album:<album_id>" album id is after the first 14 chars
            "uri": f"spotify:album:albumid-{index}",
            "album_type": "album",
            "artists": [{"name": f"artist-{index}", "id": f"artistid-{index}"}],
            "available_markets": markets,
        },
    }

def test_track_id_dict_basic_mapping():
    #make 2 sample tracks
    tracks = [make_sample_track(0), make_sample_track(1, markets=["US", "CA", "MX"])]

    #out has a list of 2 dictionaries
    out = track_id_dict(tracks)

    #verify output structure and content
    assert isinstance(out, list)
    assert len(out) == 2

    #verify track 0's contents
    first = out[0]
    assert first["track_name"] == "track-0"
    assert first["track_id"] == "id-0"
    assert first["album_name"] == "album-0"
    # album_id should be the part after "spotify:album:"
    assert first["album_id"] == "albumid-0"
    assert first["album_type"] == "album"
    assert first["artist_name"] == "artist-0"
    assert first["artist_id"] == "artistid-0"
    assert first["markets"] == ["US", "GB", "FR"]
    assert first["duration_ms"] == 100
    assert first["popularity"] == 50

    #verify track 1's contents
    second = out[1]
    assert second["track_name"] == "track-1"
    assert second["track_id"] == "id-1"
    assert second["album_name"] == "album-1"
    assert second["album_id"] == "albumid-1"
    assert second["album_type"] == "album"
    assert second["artist_name"] == "artist-1"
    assert second["artist_id"] == "artistid-1"
    assert second["markets"] == ["US", "CA", "MX"]
    assert second["duration_ms"] == 101
    assert second["popularity"] == 51
