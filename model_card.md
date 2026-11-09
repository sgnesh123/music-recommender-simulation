# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

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

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
