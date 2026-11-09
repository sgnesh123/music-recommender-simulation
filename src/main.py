"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

# --- User taste profiles ---

HIGH_ENERGY_POP = {
    "favorite_genre": "pop",
    "favorite_mood": "intense",
    "target_energy": 0.92,
    "target_valence": 0.78,
}

CHILL_LOFI = {
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.38,
    "target_valence": 0.58,
}

DEEP_INTENSE_ROCK = {
    "favorite_genre": "rock",
    "favorite_mood": "intense",
    "target_energy": 0.90,
    "target_valence": 0.40,
}

def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Taste profile
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.70,
        "target_valence": 0.75,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    width = 60
    print()
    print("=" * width)
    print("TOP RECOMMENDATIONS".center(width))
    print("=" * width)
    print(
        f"Profile: genre={user_prefs['favorite_genre']}, mood={user_prefs['favorite_mood']}, "
        f"energy={user_prefs['target_energy']:.2f}, valence={user_prefs['target_valence']:.2f}"
    )
    print("-" * width)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.2f} / 10")
        print("   Reasons:")
        for reason in explanation.split("; "):
            print(f"     - {reason}")

    print()
    print("=" * width)


if __name__ == "__main__":
    main()
