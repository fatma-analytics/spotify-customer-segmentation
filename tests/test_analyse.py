import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pandas as pd  # noqa: E402

from analyse import FEATURES, name_segment, prepare  # noqa: E402


def test_one_row_per_track_and_no_missing_features():
    tracks, quality = prepare()
    assert tracks["track_id"].is_unique
    assert tracks[FEATURES].notna().all().all()
    assert quality["titres_uniques"] == len(tracks)


def test_segment_names_follow_strongest_features():
    c = pd.Series({f: 0.0 for f in FEATURES})
    c["acousticness"], c["energy"] = 1.6, -1.5
    assert name_segment(c) == "Acoustique & calme"
