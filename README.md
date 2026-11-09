# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

---

## How The System Works

Real-world recommenders such as Spotify and YouTube work in three parts. The **input data** has two kinds: item attributes (genre, tempo, audio features) and user interaction signals. Those signals can be explicit, like likes, or implicit, like plays, skips, and playlist adds. **User preferences** are not typed in by the user. The system learns them from interaction history, often as a numeric "taste" vector, using collaborative filtering (finding users with similar behavior) and content-based filtering (finding items with similar attributes). **Ranking and selection** happens in stages. A fast step pulls a few hundred candidate items from millions. A trained model then predicts how likely you are to engage with each one, and the top-scoring items are shown.

My version is a simplified, content-based model with no learning. Its **input data** is the song catalog in `data/songs.csv`. **User preferences** are stated directly in a taste profile instead of being learned from behavior. **Ranking and selection** uses a hand-designed scoring rule that judges one song at a time against the profile. Points are split roughly half and half between label matches (genre and mood) and audio-feature closeness (energy and valence). A related label, such as "pop" for an "indie pop" fan, earns partial credit. For audio features, a song earns more points the *closer* it is to the user's target, rather than for higher or lower values, with closeness normalized by each feature's range in the catalog. Every song is scored, the list is sorted from highest to lowest score, and the top *k* songs are returned as recommendations.

**`Song` features**
- `genre`
- `mood`
- `energy`
- `valence`

**`UserProfile` features**
- `favorite_genre`
- `favorite_mood`
- `target_energy`
- `target_valence`

### Algorithm Recipe

Each song is scored out of **10 points**: 5 for label matches and 5 for audio-feature closeness.

| Feature | Max points | Full points | Partial credit |
|---|---|---|---|
| Genre | 3.0 | Exact match | 1.5 for a related genre |
| Mood | 2.0 | Exact match | 1.0 for a related mood |
| Energy | 3.0 | Song value equals `target_energy` | Scaled by closeness |
| Valence | 2.0 | Song value equals `target_valence` | Scaled by closeness |

1. **Genre and mood.** Award full points for an exact match, half points for a related label, and 0 otherwise. Related labels come from a small lookup table:
   - Genres: pop ↔ indie pop
   - Moods: {happy, playful, carefree, euphoric}, {chill, relaxed, focused}, {sad, melancholic, moody}, {intense, angry}
2. **Energy and valence.** Reward closeness to the target, not higher or lower values:
   `points = weight × max(0, 1 − |song_value − target| / feature_range)`
   The range comes from the catalog: energy = 0.75 (0.22–0.97) and valence = 0.68 (0.20–0.88).
3. **Total.** Add the four feature scores.
4. **Selection.** Score every song, sort from highest to lowest, and return the top *k*.

### Potential Biases

- **Genre over-prioritization.** Genre is the single largest category (3 points). A same-genre song with the wrong mood (e.g., a pop "intense" track for a pop/happy user) can outrank a cross-genre song that fits the user's mood and energy well.
- **Catalog imbalance.** Most genres have only one song, while lofi has three. Fans of underrepresented genres get at most one genre match, so their results depend mostly on mood and audio features.
- **Hand-picked related labels.** Partial credit depends on groupings I chose. Those groupings reflect my judgment, not data. Labels left out of a group (e.g., "nostalgic" or "romantic") never earn partial credit.
- **No penalty for poor matches.** Closeness points rarely reach 0, so even a poor match collects some points. That narrows the score gap between good and bad songs.
- **Filter bubble.** The system always recommends songs most similar to the stated profile. It never explores, so users aren't shown anything outside their usual taste.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main` for the default pop/happy taste profile:

```
============================================================
                    TOP RECOMMENDATIONS
============================================================
Profile: genre=pop, mood=happy, energy=0.70, valence=0.75
------------------------------------------------------------

1. Sunrise City by Neon Echo
   Score: 9.26 / 10
   Reasons:
     - genre exact match (pop): +3.00
     - mood exact match (happy): +2.00
     - energy 0.82 vs target 0.70: +2.52
     - valence 0.84 vs target 0.75: +1.74

2. Rooftop Lights by Indigo Parade
   Score: 8.08 / 10
   Reasons:
     - genre related match (indie pop): +1.50
     - mood exact match (happy): +2.00
     - energy 0.76 vs target 0.70: +2.76
     - valence 0.81 vs target 0.75: +1.82

3. Gym Hero by Max Pulse
   Score: 7.02 / 10
   Reasons:
     - genre exact match (pop): +3.00
     - mood no match (intense): +0.00
     - energy 0.93 vs target 0.70: +2.08
     - valence 0.77 vs target 0.75: +1.94

4. Fuego Lento by Sol Morena
   Score: 5.22 / 10
   Reasons:
     - genre no match (latin): +0.00
     - mood related match (playful): +1.00
     - energy 0.80 vs target 0.70: +2.60
     - valence 0.88 vs target 0.75: +1.62

5. Island Sunday by Roots Harbor
   Score: 5.20 / 10
   Reasons:
     - genre no match (reggae): +0.00
     - mood related match (carefree): +1.00
     - energy 0.58 vs target 0.70: +2.52
     - valence 0.86 vs target 0.75: +1.68

============================================================
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



