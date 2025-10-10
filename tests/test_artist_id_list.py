
import pytest

from assets.artist import artist_id_list

def test_artist_id_list_dedup_and_order_irrelevant():
    # function returns a list-from-set (order not guaranteed); verify by set
    # should not return any dupes

    tracks = [
        {"artists": [{"id": "A"}]},
        {"artists": [{"id": "B"}]},
        {"artists": [{"id": "A"}]},  # dup
        {"artists": [{"id": "C"}]},
    ]
    out = artist_id_list(tracks)

    print(out)
    assert set(out) == {"A", "B", "C"}

    #to call: python -m pytest -q tests\test_artist_id_list.py
