# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**: it matches songs to the vibe you ask for.

---

## 2. Intended Use  

### Goal / Task

VibeMatch suggests songs a listener is likely to enjoy. It doesn't learn or predict anything from listening history. It takes a taste profile (favorite genre, favorite mood, ideal energy, ideal valence) and scores every song against it. Then it returns the top 5 matches, each with a reason for why it was picked.

### Intended Use

- A classroom project for learning how recommender systems work.
- Exploring how scoring rules and weights change what gets recommended.
- Testing ideas about bias and fairness on a small, easy-to-read dataset.

It assumes the user can describe their taste with one genre, one mood, and two numbers.

### Non-Intended Use

- It is not meant for real listeners or a real music app. The catalog has only 20 made-up songs.
- It should not be used to judge whether a song or artist is "good." It only measures how close a song is to one profile.
- It should not be used to make decisions about people. It knows nothing about who the user is.
- It is not a good fit for listeners whose taste mixes several genres or moods. It can only hold one of each.

---

## 3. How the Model Works  

Think of the recommender as a judge holding a scorecard. It compares every song in the catalog to the listener's taste and hands out up to 10 points. Then it recommends the songs with the highest scores.

**What it looks at in each song.** It uses four things: the song's **genre** (like pop or jazz), its **mood** (like happy or chill), its **energy** (how calm or intense it feels), and its **valence** (how positive or gloomy it sounds). Energy and valence are numbers from 0 to 1.

**What it knows about the listener.** The listener has a taste profile: a favorite genre, a favorite mood, an ideal energy level, and an ideal valence level.

**How it hands out points.**
- **Genre (up to 3 points):** A song in the listener's favorite genre gets all 3 points. A closely related genre, like indie pop for a pop fan, gets half (1.5). Anything else gets 0.
- **Mood (up to 2 points):** The same idea. An exact mood match earns 2 points. A related mood, like "playful" for someone who wants "happy," earns 1.
- **Energy (up to 3 points) and valence (up to 2 points):** Here the system rewards songs for being *close* to what the listener wants, not for being higher or lower. If you want medium energy, a medium-energy song scores best, and very calm and very intense songs both lose points. The further a song is from the target, the fewer points it gets.

The label matches (genre and mood) and the sound-based features (energy and valence) are each worth about half the total. Neither side can completely outweigh the other. After every song is scored, the list is sorted from highest to lowest, and the top few are recommended. Each recommendation shows its score and a breakdown of where its points came from, so the listener can see *why* it was picked.

**Changes from the starter logic.** The starter returned the first few songs in the file without scoring them. I added the point system above. I chose four features out of the catalog's attributes and left out tempo, danceability, and acousticness, because they mostly measured the same thing as energy. I added valence, because it was the one feature that told me something new: whether a song feels upbeat or dark. I also added partial credit for related genres and moods, so near-misses aren't treated as total misses.

---

## 4. Data  

- **Size:** 20 songs in `data/songs.csv`. The starter file had 10. I added 10 more to cover new genres and moods.
- **Variety:** 17 genres (like pop, lofi, rock, jazz, metal, classical, and reggae) and 16 moods (like happy, chill, intense, sad, and romantic).
- **Features:** Each song has a title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness. VibeMatch uses only four of these: genre, mood, energy, and valence.

**Limits:**
- The dataset is tiny. Most genres have only one song. Lofi has three, and pop has two.
- The songs are made up. Their numbers were chosen by hand, not measured from real audio.
- Each song has just one genre and one mood. Real songs often fit several.
- Many parts of taste are missing, such as lyrics, language, era, artist popularity, and what listeners actually played or skipped.

---

## 5. Strengths  

- **Listeners with common tastes get great results.** The Chill Lofi profile got all three lofi songs at the top, with near-perfect scores.
- **The energy setting works.** A high-energy profile gets loud songs, and a low-energy profile gets calm ones. The two lists don't overlap at all.
- **"Closer is better" scoring works.** A medium-energy listener isn't pushed toward the loudest or quietest songs.
- **Partial credit helps.** Indie pop counts as close to pop, so Rooftop Lights ranks well for a pop fan.
- **Every pick is explained.** Each result shows exactly where its points came from, so it's easy to see why a song was chosen.

---

## 6. Limitations and Bias 

The system serves listeners with mainstream, upbeat tastes much better than listeners with dark or niche tastes. When I built an ideal user for each song in the catalog and averaged that user's top 5 recommendations (excluding the song itself), lofi/chill and pop/happy listeners averaged 6.3–7.0 out of 10, but metal/angry, classical/melancholic, and folk/sad listeners averaged only 3.8–4.0. The main cause is the catalog: lofi has three songs and pop has two, while metal, classical, folk, and most other genres have just one, so a niche listener runs out of genre matches after a single song. The related-label groups I hand-picked make this worse, because moods like nostalgic, romantic, confident, and soulful aren't in any group, so those listeners can never earn partial credit either. As a result, users with less common tastes get weaker and more generic recommendations, while the system appears to work best for the listeners who were already best represented.

**Other patterns I noticed:**
- **Labels can beat sound.** A pop song in the wrong mood (Gym Hero) still shows up for Happy Pop and even Deep Intense Rock listeners.
- **Capital letters break matching.** "Pop" doesn't match "pop," so a small typo wipes out the genre and mood points.
- **Bad input isn't caught.** An energy target of 1.5 is accepted without any warning.
- **Filter bubble.** The system only picks songs similar to the profile. It never suggests something new to try.

---

## 7. Evaluation  

**Summary:** I tested the system in three ways.
1. I ran four normal profiles and checked whether each top 5 felt right.
2. I compared the profiles in pairs to see what changed and why.
3. I ran six tricky edge-case profiles to try to break the scoring.

I also built an "ideal listener" for every song to check which tastes get the best results (see Limitations and Bias).

### Profiles I Tested

I tested four "normal" listener profiles, then six edge-case profiles (described further down) designed to trick the system. For each normal profile I checked whether the top 5 felt right for that listener: the right kind of songs at the top, clearly wrong songs left out, and reasons that made sense.

| Profile | Genre | Mood | Energy | Valence | Top 5 recommendations |
|---|---|---|---|---|---|
| Default Pop/Happy | pop | happy | 0.70 | 0.75 | Sunrise City, Rooftop Lights, Gym Hero, Fuego Lento, Island Sunday |
| High-Energy Pop | pop | intense | 0.92 | 0.78 | Gym Hero, Sunrise City, Storm Runner, Rooftop Lights, Laser Tide |
| Chill Lofi | lofi | chill | 0.38 | 0.58 | Library Rain, Midnight Coding, Focus Flow, Spacewalk Thoughts, Coffee Shop Stories |
| Deep Intense Rock | rock | intense | 0.90 | 0.40 | Storm Runner, Gym Hero, Iron Collapse, Night Drive Loop, Concrete Verses |

### What Surprised Me

**"Gym Hero" shows up almost everywhere.** It made the top 3 for three of the four profiles, including the Happy Pop listener, who never asked for a workout anthem. Think of the scorecard as a judge giving points in four categories. Gym Hero is a pop song, so it collects the full 3 "right genre" points from any pop fan. Its upbeat feel (valence) is close to what a happy listener wants, so it collects almost all of those points too. It loses only the 2 mood points, because it's "intense" rather than "happy." Even with that loss, it still scores higher than songs that have the right mood but the wrong genre. In short, the system rewards Gym Hero for being *pop* more than it penalizes it for being the *wrong kind* of pop.

**A dark rock fan gets a cheerful pop song at #2.** For the Deep Intense Rock listener, Gym Hero (bright, upbeat pop) beat Iron Collapse (dark, aggressive metal). Both are high-energy. Gym Hero is labeled "intense," an exact mood match worth 2 points, while Iron Collapse is labeled "angry," a related mood worth only 1. That single point made the difference, even though Iron Collapse is much closer to the dark feel this listener wanted. The labels mattered more than how the songs actually sound.

**Chill Lofi was the most satisfying result.** All three lofi songs took the top 3 spots with near-perfect scores, followed by other calm songs (ambient, jazz). It worked best because lofi is the genre with the most songs in the catalog.

### Comparing the Profiles

- **Default Pop/Happy vs. High-Energy Pop:** Both like pop, so the same pop songs appear in both lists, but the order flips. The happy listener gets Sunrise City first. When the mood changes to "intense" and energy goes up to 0.92, Gym Hero jumps from #3 to #1, and the other new arrivals are loud songs from other genres (Storm Runner, Laser Tide). This makes sense: changing only the mood and energy kept the genre the same and pushed the list toward louder, harder songs.
- **Default Pop/Happy vs. Chill Lofi:** These lists share no songs at all. The pop list is full of bright, mid-to-high-energy tracks, while the lofi list is all quiet, low-energy songs (energy 0.28–0.42). This makes sense because the two profiles differ on every setting at once: genre, mood, and energy level.
- **Default Pop/Happy vs. Deep Intense Rock:** The only song in both lists is Gym Hero. The rock list swaps cheerful songs for darker ones (Iron Collapse, Night Drive Loop) because the rock listener's valence target is low (0.40). It makes sense that the lists are so different, but Gym Hero appearing in both shows how a pop song with high energy can sneak into very different tastes.
- **High-Energy Pop vs. Chill Lofi:** These are opposites, and the results are too. One list is all high-energy songs (0.76–0.95), and the other is all calm ones (0.28–0.42). This is the clearest sign that the energy setting works: moving the energy target from high to low completely swaps the type of music.
- **High-Energy Pop vs. Deep Intense Rock:** Both want very high energy and an "intense" mood, so they share Gym Hero and Storm Runner, just in reverse order. The genre preference decides which one comes first. The difference is in feel: the pop listener's lower picks are bright (Sunrise City, Laser Tide), while the rock listener's are dark (Iron Collapse, Night Drive Loop). That matches their valence targets (0.78 vs. 0.40).
- **Chill Lofi vs. Deep Intense Rock:** No overlap. The lofi list is quiet and mellow, and the rock list is loud and heavy. This makes sense because the two profiles are at opposite ends of the energy scale and have unrelated genres and moods.

### Edge-Case and Adversarial Profiles

I designed six profiles to try to trick the scoring logic or produce unexpected results. For each one, I ran the recommender and looked at the top 5.

| Profile | What it tests |
|---|---|
| Conflicting: High-Energy Sad | Wants sad folk at 0.90 energy, a combination that doesn't exist in the catalog. |
| Unknown Labels | The genre (k-pop) and mood (hopeful) don't exist in the catalog. |
| Out-of-Range Targets | Energy 1.50 and valence −0.50, outside the valid 0–1 range. |
| Capitalized Labels | The same taste as the default pop/happy profile, but typed as "Pop" and "HAPPY". |
| Genre vs. Sound Mismatch | Wants classical music that is euphoric and very high-energy. |
| Dead Center | Pop + chill with energy and valence of 0.50. No song is both pop and chill. |

#### Conflicting: High-Energy Sad

```
============================================================
                CONFLICTING: HIGH-ENERGY SAD
============================================================
Profile: genre=folk, mood=sad, energy=0.90, valence=0.20
------------------------------------------------------------

1. Paper Boats by June Hollow
   Score: 7.60 / 10
   Reasons:
     - genre exact match (folk): +3.00
     - mood exact match (sad): +2.00
     - energy 0.30 vs target 0.90: +0.60
     - valence 0.20 vs target 0.20: +2.00

2. Iron Collapse by Grave Engine
   Score: 4.66 / 10
   Reasons:
     - genre no match (metal): +0.00
     - mood no match (angry): +0.00
     - energy 0.97 vs target 0.90: +2.72
     - valence 0.22 vs target 0.20: +1.94

3. Night Drive Loop by Neon Echo
   Score: 4.55 / 10
   Reasons:
     - genre no match (synthwave): +0.00
     - mood related match (moody): +1.00
     - energy 0.75 vs target 0.90: +2.40
     - valence 0.49 vs target 0.20: +1.15

4. Storm Runner by Voltline
   Score: 4.14 / 10
   Reasons:
     - genre no match (rock): +0.00
     - mood no match (intense): +0.00
     - energy 0.91 vs target 0.90: +2.96
     - valence 0.48 vs target 0.20: +1.18

5. Concrete Verses by Block Theory
   Score: 3.28 / 10
   Reasons:
     - genre no match (hip hop): +0.00
     - mood no match (confident): +0.00
     - energy 0.78 vs target 0.90: +2.52
     - valence 0.62 vs target 0.20: +0.76

============================================================
```

**Observation:** The label points win. *Paper Boats* comes first even though its energy (0.30) is far from the target, because genre, mood, and valence together outweigh energy. The rest of the list is filled by loud, dark songs. That means a "sad" listener is offered angry metal (*Iron Collapse*) at #2.

#### Unknown Labels

```
============================================================
         UNKNOWN LABELS (GENRE/MOOD NOT IN CATALOG)
============================================================
Profile: genre=k-pop, mood=hopeful, energy=0.70, valence=0.75
------------------------------------------------------------

1. Rooftop Lights by Indigo Parade
   Score: 4.58 / 10
   Reasons:
     - genre no match (indie pop): +0.00
     - mood no match (happy): +0.00
     - energy 0.76 vs target 0.70: +2.76
     - valence 0.81 vs target 0.75: +1.82

2. Concrete Verses by Block Theory
   Score: 4.30 / 10
   Reasons:
     - genre no match (hip hop): +0.00
     - mood no match (confident): +0.00
     - energy 0.78 vs target 0.70: +2.68
     - valence 0.62 vs target 0.75: +1.62

3. Sunrise City by Neon Echo
   Score: 4.26 / 10
   Reasons:
     - genre no match (pop): +0.00
     - mood no match (happy): +0.00
     - energy 0.82 vs target 0.70: +2.52
     - valence 0.84 vs target 0.75: +1.74

4. Dusty Porch Swing by Hollow Creek
   Score: 4.25 / 10
   Reasons:
     - genre no match (country): +0.00
     - mood no match (nostalgic): +0.00
     - energy 0.55 vs target 0.70: +2.40
     - valence 0.70 vs target 0.75: +1.85

5. Fuego Lento by Sol Morena
   Score: 4.22 / 10
   Reasons:
     - genre no match (latin): +0.00
     - mood no match (playful): +0.00
     - energy 0.80 vs target 0.70: +2.60
     - valence 0.88 vs target 0.75: +1.62

============================================================
```

**Observation:** No song can earn label points, so the ranking falls back on energy and valence alone. The system doesn't crash, but every score is capped at 5/10 and the top 5 are bunched within 0.36 points, so the ranking is weak.

#### Out-of-Range Targets

```
============================================================
                    OUT-OF-RANGE TARGETS
============================================================
Profile: genre=pop, mood=happy, energy=1.50, valence=-0.50
------------------------------------------------------------

1. Sunrise City by Neon Echo
   Score: 5.28 / 10
   Reasons:
     - genre exact match (pop): +3.00
     - mood exact match (happy): +2.00
     - energy 0.82 vs target 1.50: +0.28
     - valence 0.84 vs target -0.50: +0.00

2. Gym Hero by Max Pulse
   Score: 3.72 / 10
   Reasons:
     - genre exact match (pop): +3.00
     - mood no match (intense): +0.00
     - energy 0.93 vs target 1.50: +0.72
     - valence 0.77 vs target -0.50: +0.00

3. Rooftop Lights by Indigo Parade
   Score: 3.54 / 10
   Reasons:
     - genre related match (indie pop): +1.50
     - mood exact match (happy): +2.00
     - energy 0.76 vs target 1.50: +0.04
     - valence 0.81 vs target -0.50: +0.00

4. Laser Tide by Pulsewave
   Score: 1.80 / 10
   Reasons:
     - genre no match (edm): +0.00
     - mood related match (euphoric): +1.00
     - energy 0.95 vs target 1.50: +0.80
     - valence 0.80 vs target -0.50: +0.00

5. Fuego Lento by Sol Morena
   Score: 1.20 / 10
   Reasons:
     - genre no match (latin): +0.00
     - mood related match (playful): +1.00
     - energy 0.80 vs target 1.50: +0.20
     - valence 0.88 vs target -0.50: +0.00

============================================================
```

**Observation:** There is no input validation. Every song gets 0 valence points, and energy points shrink toward 0. The system silently turns into a genre/mood matcher instead of warning about bad input.

#### Capitalized Labels

```
============================================================
                     CAPITALIZED LABELS
============================================================
Profile: genre=Pop, mood=HAPPY, energy=0.70, valence=0.75
------------------------------------------------------------

1. Rooftop Lights by Indigo Parade
   Score: 4.58 / 10
   Reasons:
     - genre no match (indie pop): +0.00
     - mood no match (happy): +0.00
     - energy 0.76 vs target 0.70: +2.76
     - valence 0.81 vs target 0.75: +1.82

2. Concrete Verses by Block Theory
   Score: 4.30 / 10
   Reasons:
     - genre no match (hip hop): +0.00
     - mood no match (confident): +0.00
     - energy 0.78 vs target 0.70: +2.68
     - valence 0.62 vs target 0.75: +1.62

3. Sunrise City by Neon Echo
   Score: 4.26 / 10
   Reasons:
     - genre no match (pop): +0.00
     - mood no match (happy): +0.00
     - energy 0.82 vs target 0.70: +2.52
     - valence 0.84 vs target 0.75: +1.74

4. Dusty Porch Swing by Hollow Creek
   Score: 4.25 / 10
   Reasons:
     - genre no match (country): +0.00
     - mood no match (nostalgic): +0.00
     - energy 0.55 vs target 0.70: +2.40
     - valence 0.70 vs target 0.75: +1.85

5. Fuego Lento by Sol Morena
   Score: 4.22 / 10
   Reasons:
     - genre no match (latin): +0.00
     - mood no match (playful): +0.00
     - energy 0.80 vs target 0.70: +2.60
     - valence 0.88 vs target 0.75: +1.62

============================================================
```

**Observation:** **This tricks the system.** Matching is case-sensitive, so *Sunrise City* (pop/happy) gets no label points and drops from 9.26 to 4.26. The output is identical to the Unknown Labels profile, which shows that a typo is treated the same as an unknown genre.

#### Genre vs. Sound Mismatch

```
============================================================
                  GENRE VS. SOUND MISMATCH
============================================================
Profile: genre=classical, mood=euphoric, energy=0.95, valence=0.85
------------------------------------------------------------

1. Laser Tide by Pulsewave
   Score: 6.85 / 10
   Reasons:
     - genre no match (edm): +0.00
     - mood exact match (euphoric): +2.00
     - energy 0.95 vs target 0.95: +3.00
     - valence 0.80 vs target 0.85: +1.85

2. Sunrise City by Neon Echo
   Score: 5.45 / 10
   Reasons:
     - genre no match (pop): +0.00
     - mood related match (happy): +1.00
     - energy 0.82 vs target 0.95: +2.48
     - valence 0.84 vs target 0.85: +1.97

3. Fuego Lento by Sol Morena
   Score: 5.31 / 10
   Reasons:
     - genre no match (latin): +0.00
     - mood related match (playful): +1.00
     - energy 0.80 vs target 0.95: +2.40
     - valence 0.88 vs target 0.85: +1.91

4. Rooftop Lights by Indigo Parade
   Score: 5.12 / 10
   Reasons:
     - genre no match (indie pop): +0.00
     - mood related match (happy): +1.00
     - energy 0.76 vs target 0.95: +2.24
     - valence 0.81 vs target 0.85: +1.88

5. Gym Hero by Max Pulse
   Score: 4.68 / 10
   Reasons:
     - genre no match (pop): +0.00
     - mood no match (intense): +0.00
     - energy 0.93 vs target 0.95: +2.92
     - valence 0.77 vs target 0.85: +1.76

============================================================
```

**Observation:** No classical song appears in the top 5. The only classical track (*Winter Sonata*) is calm and melancholic, so mood and sound outweigh the 3 genre points. That's reasonable here, and it shows genre can't override everything.

#### Dead Center

```
============================================================
              DEAD CENTER (ALL MIDDLE VALUES)
============================================================
Profile: genre=pop, mood=chill, energy=0.50, valence=0.50
------------------------------------------------------------

1. Midnight Coding by LoRoom
   Score: 6.50 / 10
   Reasons:
     - genre no match (lofi): +0.00
     - mood exact match (chill): +2.00
     - energy 0.42 vs target 0.50: +2.68
     - valence 0.56 vs target 0.50: +1.82

2. Library Rain by Paper Lanterns
   Score: 6.11 / 10
   Reasons:
     - genre no match (lofi): +0.00
     - mood exact match (chill): +2.00
     - energy 0.35 vs target 0.50: +2.40
     - valence 0.60 vs target 0.50: +1.71

3. Sunrise City by Neon Echo
   Score: 5.72 / 10
   Reasons:
     - genre exact match (pop): +3.00
     - mood no match (happy): +0.00
     - energy 0.82 vs target 0.50: +1.72
     - valence 0.84 vs target 0.50: +1.00

4. Spacewalk Thoughts by Orbit Bloom
   Score: 5.68 / 10
   Reasons:
     - genre no match (ambient): +0.00
     - mood exact match (chill): +2.00
     - energy 0.28 vs target 0.50: +2.12
     - valence 0.65 vs target 0.50: +1.56

5. Gym Hero by Max Pulse
   Score: 5.49 / 10
   Reasons:
     - genre exact match (pop): +3.00
     - mood no match (intense): +0.00
     - energy 0.93 vs target 0.50: +1.28
     - valence 0.77 vs target 0.50: +1.21

============================================================
```

**Observation:** Chill lofi songs (mood match plus close sound) narrowly beat pop songs (genre match only). *Gym Hero*, an intense high-energy track, still makes #5 for a chill listener on its genre points alone.

---

## 8. Future Work  

1. **Clean up user input.** Make genre and mood matching ignore capital letters. Check that energy and valence targets are between 0 and 1.
2. **Add variety to the top 5.** Limit how many songs from the same genre can appear, and save one spot for something new, so the list isn't a filter bubble.
3. **Grow and balance the catalog.** Add more songs to genres that have only one, and put every mood into a related-mood group, so niche listeners get results as good as pop and lofi fans.

---

## 9. Personal Reflection  

**What I learned.** A recommender is really a set of choices about what matters. Picking the features and the weights *is* the design. I also learned that more features aren't always better. Tempo, danceability, and acousticness mostly measured the same thing as energy, so using all of them would have counted one idea four times.

**What surprised me.** Small rules had big effects. One point of mood credit was enough to put a cheerful pop song (Gym Hero) above a dark metal song for a rock fan. A capital letter in "Pop" was enough to wipe out a perfect match. I was also surprised that the system worked best for the tastes with the most songs. It looked fair on paper, but the data made it unfair.

**How it changed my thinking.** I now see music apps differently. When an app keeps showing me the same kind of song, it may not be because I love it. It may be because that's what the scoring rules and the catalog favor. Real apps are far more complex than mine, but they still make the same kinds of trade-offs between matching my taste and helping me discover something new.  
