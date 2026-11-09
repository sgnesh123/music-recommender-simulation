import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into dicts, converting numeric fields to int/float."""
    int_fields = {"id"}
    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

# --- Algorithm Recipe constants (see "Algorithm Recipe" in README.md) ---

GENRE_WEIGHT = 3.0
MOOD_WEIGHT = 2.0
ENERGY_WEIGHT = 3.0
VALENCE_WEIGHT = 2.0
PARTIAL_CREDIT = 0.5  # related labels earn half points

# Feature ranges in the catalog (max - min), used to normalize closeness
ENERGY_RANGE = 0.75   # 0.22 - 0.97
VALENCE_RANGE = 0.68  # 0.20 - 0.88

RELATED_GENRES = [
    {"pop", "indie pop"},
]

RELATED_MOODS = [
    {"happy", "playful", "carefree", "euphoric"},
    {"chill", "relaxed", "focused"},
    {"sad", "melancholic", "moody"},
    {"intense", "angry"},
]


def _label_points(preferred: str, actual: str, weight: float, groups: List[set]) -> Tuple[float, str]:
    """Full points for an exact match, partial credit for a related label, else 0."""
    if actual == preferred:
        return weight, "exact match"
    if any(preferred in group and actual in group for group in groups):
        return weight * PARTIAL_CREDIT, "related match"
    return 0.0, "no match"


def _closeness_points(target: float, actual: float, weight: float, feature_range: float) -> float:
    """Points scaled by how close the value is to the target, normalized by the feature's range."""
    closeness = max(0.0, 1 - abs(actual - target) / feature_range)
    return weight * closeness


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against the taste profile, returning (total score, list of per-feature reasons)."""
    reasons = []

    genre_pts, genre_kind = _label_points(
        user_prefs["favorite_genre"], song["genre"], GENRE_WEIGHT, RELATED_GENRES
    )
    reasons.append(f"genre {genre_kind} ({song['genre']}): +{genre_pts:.2f}")

    mood_pts, mood_kind = _label_points(
        user_prefs["favorite_mood"], song["mood"], MOOD_WEIGHT, RELATED_MOODS
    )
    reasons.append(f"mood {mood_kind} ({song['mood']}): +{mood_pts:.2f}")

    energy_pts = _closeness_points(
        user_prefs["target_energy"], song["energy"], ENERGY_WEIGHT, ENERGY_RANGE
    )
    reasons.append(
        f"energy {song['energy']:.2f} vs target {user_prefs['target_energy']:.2f}: +{energy_pts:.2f}"
    )

    valence_pts = _closeness_points(
        user_prefs["target_valence"], song["valence"], VALENCE_WEIGHT, VALENCE_RANGE
    )
    reasons.append(
        f"valence {song['valence']:.2f} vs target {user_prefs['target_valence']:.2f}: +{valence_pts:.2f}"
    )

    score = genre_pts + mood_pts + energy_pts + valence_pts
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song and return the top k as (song, score, explanation), highest score first."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))

    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
