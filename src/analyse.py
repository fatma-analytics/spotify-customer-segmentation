"""Segmentation du catalogue Spotify : profils sonores, genres et popularité.

Usage : python src/analyse.py
Entrée  : data/spotify_songs.csv (TidyTuesday 2020-01-21, données Spotify via spotifyr)
Sorties : reports/results/*.csv, reports/results/resume.json, reports/figures/*.png
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.cluster import KMeans  # noqa: E402
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestClassifier  # noqa: E402
from sklearn.metrics import confusion_matrix, silhouette_score  # noqa: E402
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_predict, cross_val_score  # noqa: E402
from sklearn.preprocessing import StandardScaler  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "spotify_songs.csv"
FIG = ROOT / "reports" / "figures"
RES = ROOT / "reports" / "results"
SEED = 42

FEATURES = ["danceability", "energy", "loudness", "speechiness", "acousticness",
            "instrumentalness", "liveness", "valence", "tempo"]
LABELS_FR = {"danceability": "Dansabilité", "energy": "Énergie", "loudness": "Volume",
             "speechiness": "Parole", "acousticness": "Acoustique", "instrumentalness": "Instrumental",
             "liveness": "Live", "valence": "Positivité", "tempo": "Tempo"}
BLUE, GREY, ORANGE = "#1f4e79", "#9aa5b1", "#d97904"
plt.rcParams.update({"figure.dpi": 150, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.titleweight": "bold", "font.size": 9.5})
SOURCE = "Source : Spotify via spotifyr (TidyTuesday, janvier 2020). 28 356 titres, 6 genres de playlists."


def save(fig, name):
    FIG.mkdir(parents=True, exist_ok=True)
    fig.text(0.01, -0.09, SOURCE, fontsize=7, color="grey")
    fig.savefig(FIG / name, bbox_inches="tight")
    plt.close(fig)


# 1. Préparation et qualité des données -------------------------------------------
def prepare() -> tuple[pd.DataFrame, dict]:
    raw = pd.read_csv(DATA)
    quality = {
        "lignes_brutes": len(raw),
        "titres_uniques": int(raw["track_id"].nunique()),
        "doublons_titre_playlist": int(len(raw) - raw["track_id"].nunique()),
        "valeurs_manquantes": int(raw[FEATURES + ["track_name"]].isna().any(axis=1).sum()),
        "titres_popularite_zero": int((raw.drop_duplicates("track_id")["track_popularity"] == 0).sum()),
    }
    # Un titre peut figurer dans plusieurs playlists (et genres) : on garde une ligne par titre,
    # avec le genre le plus fréquent parmi ses playlists.
    main_genre = (raw.groupby(["track_id", "playlist_genre"]).size().rename("n").reset_index()
                  .sort_values(["track_id", "n"], ascending=[True, False])
                  .drop_duplicates("track_id").set_index("track_id")["playlist_genre"])
    tracks = raw.drop_duplicates("track_id").set_index("track_id")
    tracks["genre"] = main_genre
    tracks["nb_genres"] = raw.groupby("track_id")["playlist_genre"].nunique()
    tracks["annee"] = pd.to_numeric(tracks["track_album_release_date"].str[:4], errors="coerce")
    tracks = tracks.dropna(subset=FEATURES).reset_index()
    quality["titres_dans_plusieurs_genres"] = int((tracks["nb_genres"] > 1).sum())
    quality["titres_analyses"] = len(tracks)
    return tracks, quality


# 2. Segmentation des profils sonores ----------------------------------------------
def segment(tracks: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    X = StandardScaler().fit_transform(tracks[FEATURES])
    scores = {}
    for k in range(3, 9):
        lab = KMeans(k, n_init=10, random_state=SEED).fit_predict(X)
        scores[k] = silhouette_score(X, lab, sample_size=10000, random_state=SEED)
    k_best = max(scores, key=scores.get)
    km = KMeans(k_best, n_init=10, random_state=SEED).fit(X)
    tracks = tracks.assign(segment=km.labels_)
    centers = pd.DataFrame(km.cluster_centers_, columns=FEATURES)
    centers["segment"] = range(k_best)
    centers["nom"] = centers.apply(name_segment, axis=1)
    tracks["segment_nom"] = tracks["segment"].map(centers.set_index("segment")["nom"])
    return tracks, centers, {"k_retenu": k_best, "silhouette_par_k": {k: round(v, 3) for k, v in scores.items()}}


def name_segment(c: pd.Series) -> str:
    """Nom lisible à partir des deux caractéristiques les plus marquées (z-scores du centre)."""
    names_pos = {"danceability": "dansant", "energy": "énergique", "loudness": "fort",
                 "speechiness": "parlé / rap", "acousticness": "acoustique", "instrumentalness": "instrumental",
                 "liveness": "live", "valence": "joyeux", "tempo": "rapide"}
    names_neg = {"danceability": "peu dansant", "energy": "calme", "loudness": "doux",
                 "speechiness": "chanté", "acousticness": "électronique", "instrumentalness": "chanté",
                 "liveness": "studio", "valence": "mélancolique", "tempo": "lent"}
    z = c[FEATURES].astype(float)
    top = z.abs().sort_values(ascending=False).index[:2]
    words = [names_pos[f] if z[f] > 0 else names_neg[f] for f in top]
    return " & ".join(dict.fromkeys(words)).capitalize()


# 3. Le son permet-il de retrouver le genre ? ----------------------------------------
def genre_model(tracks: pd.DataFrame) -> tuple[pd.DataFrame, float, list]:
    clf = RandomForestClassifier(n_estimators=300, min_samples_leaf=3, random_state=SEED, n_jobs=-1)
    pred = cross_val_predict(clf, tracks[FEATURES + ["duration_ms"]], tracks["genre"],
                             cv=StratifiedKFold(5, shuffle=True, random_state=SEED))
    acc = float((pred == tracks["genre"]).mean())
    genres = sorted(tracks["genre"].unique())
    cm = pd.DataFrame(confusion_matrix(tracks["genre"], pred, labels=genres, normalize="true"),
                      index=genres, columns=genres)
    return cm, acc, genres


# 4. Le son explique-t-il la popularité ? ----------------------------------------------
def popularity(tracks: pd.DataFrame) -> dict:
    t = tracks[tracks["track_popularity"] > 0]
    y = t["track_popularity"]
    gbr = HistGradientBoostingRegressor(max_iter=300, learning_rate=0.05, random_state=SEED)
    r2_audio = cross_val_score(gbr, t[FEATURES + ["duration_ms"]], y, cv=KFold(5, shuffle=True, random_state=SEED), scoring="r2").mean()
    X_all = pd.concat([t[FEATURES + ["duration_ms", "annee"]],
                       pd.get_dummies(t["genre"], prefix="g", dtype=float)], axis=1)
    r2_all = cross_val_score(gbr, X_all, y, cv=KFold(5, shuffle=True, random_state=SEED), scoring="r2").mean()
    return {"r2_audio_seul": round(float(r2_audio), 3), "r2_audio_genre_annee": round(float(r2_all), 3)}


# 5. Graphiques ------------------------------------------------------------------------
def figures(tracks, centers, cm, acc, seg_info):
    # Profils des segments (heatmap des z-scores)
    c = centers.set_index("nom")[FEATURES].rename(columns=LABELS_FR)
    fig, ax = plt.subplots(figsize=(9, 3.8))
    im = ax.imshow(c.values, cmap="RdBu_r", vmin=-2, vmax=2, aspect="auto")
    ax.set_xticks(range(len(c.columns)), c.columns, rotation=30, ha="right")
    ax.set_yticks(range(len(c)), [f"{n} ({(tracks.segment_nom == n).mean():.0%})" for n in c.index])
    for i in range(c.shape[0]):
        for j in range(c.shape[1]):
            ax.text(j, i, f"{c.values[i, j]:+.1f}", ha="center", va="center", fontsize=7)
    fig.colorbar(im, ax=ax, label="Écart à la moyenne (écarts-types)")
    ax.set_title(f"{seg_info['k_retenu']} profils sonores dans le catalogue (part des titres entre parenthèses)")
    save(fig, "01_profils_sonores.png")

    # Composition des segments par genre
    mix = pd.crosstab(tracks["segment_nom"], tracks["genre"], normalize="index")
    fig, ax = plt.subplots(figsize=(9, 3.8))
    left = np.zeros(len(mix))
    palette = ["#1f4e79", "#5b8db8", "#a9c4de", "#d97904", "#f0b56b", "#9aa5b1"]
    for g, col in zip(mix.columns, palette, strict=True):
        ax.barh(mix.index, mix[g], left=left, color=col, label=g)
        left += mix[g].values
    ax.set_xlabel("Part des titres du segment")
    ax.set_title("Chaque profil sonore mélange plusieurs genres")
    ax.legend(ncol=6, frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.15))
    save(fig, "02_segments_par_genre.png")

    # Matrice de confusion genre
    fig, ax = plt.subplots(figsize=(5.8, 4.8))
    ax.imshow(cm.values, cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(range(len(cm)), cm.columns)
    ax.set_yticks(range(len(cm)), cm.index)
    for i in range(len(cm)):
        for j in range(len(cm)):
            ax.text(j, i, f"{cm.values[i, j]:.0%}", ha="center", va="center", fontsize=8,
                    color="white" if cm.values[i, j] > 0.5 else "black")
    ax.set_xlabel("Genre prédit à partir du son")
    ax.set_ylabel("Genre de la playlist")
    ax.set_title(f"Le son ne retrouve le genre que dans {acc:.0%} des cas")
    save(fig, "03_genre_confusion.png")

    # Popularité par segment
    order = tracks.groupby("segment_nom")["track_popularity"].median().sort_values().index
    fig, ax = plt.subplots(figsize=(9, 3.6))
    ax.boxplot([tracks.loc[tracks.segment_nom == s, "track_popularity"] for s in order],
               vert=False, tick_labels=list(order), showfliers=False,
               medianprops={"color": ORANGE, "linewidth": 2})
    ax.set_xlabel("Popularité Spotify (0-100)")
    ax.set_title("La popularité varie peu d'un profil sonore à l'autre")
    save(fig, "04_popularite_par_segment.png")


def main():
    RES.mkdir(parents=True, exist_ok=True)
    tracks, quality = prepare()
    tracks, centers, seg_info = segment(tracks)
    cm, acc, _ = genre_model(tracks)
    pop = popularity(tracks)
    figures(tracks, centers, cm, acc, seg_info)

    seg_summary = tracks.groupby("segment_nom").agg(
        titres=("track_id", "size"), popularite_mediane=("track_popularity", "median"),
        genre_principal=("genre", lambda s: s.value_counts().index[0]),
        part_genre_principal=("genre", lambda s: round(s.value_counts(normalize=True).iloc[0], 3)),
    ).sort_values("titres", ascending=False)
    seg_summary.to_csv(RES / "segments.csv")
    centers.to_csv(RES / "centres_segments.csv", index=False)
    cm.round(3).to_csv(RES / "confusion_genres.csv")
    tracks[["track_id", "track_name", "track_artist", "genre", "segment_nom", "track_popularity"]].to_csv(
        RES / "titres_segmentes.csv", index=False)

    summary = {"qualite": quality, "segmentation": seg_info, "precision_genre": round(acc, 3),
               "popularite": pop, "segments": seg_summary.reset_index().to_dict(orient="records")}
    (RES / "resume.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False, default=str))
    print(json.dumps(summary, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
