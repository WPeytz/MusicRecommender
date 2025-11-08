# Music Recommender System

A content-based music recommendation system using Spotify audio features and K-Nearest Neighbors for similarity matching.

## Features

- **Multi-feature similarity engine**: Uses 9 audio features (danceability, energy, valence, acousticness, instrumentalness, speechiness, liveness, loudness, tempo)
- **Playlist profile aggregation**: Combines multiple input tracks to create a target listening profile
- **Artist-aware boosting**: Leverages target artist hints to improve recommendations
- **Genre-aware matching**: Boosts songs from matching genres
- **Efficient KNN search**: Fast similarity computation across 89,740 unique tracks

## Dataset

- **89,740 unique tracks** across 114 genres
- Rich Spotify audio features for each track
- Artist, album, and track metadata
- Popularity scores

## Architecture

### 1. Data Preprocessing
- Removes duplicate track IDs
- Handles missing values
- Normalizes tempo and loudness features to same scale as other features
- Normalizes feature vectors to unit length for cosine similarity

### 2. Similarity Calculation
- Uses K-Nearest Neighbors with cosine metric
- Fetches top 1000 candidates (or 20x requested recommendations)
- Computes similarity based on normalized audio feature vectors

### 3. Scoring System

Final score for each candidate track:

```
base_score = cosine_similarity(input_profile, candidate)

if candidate.artist in target_artists:
    score *= 1.5  # 50% boost

if candidate.genre in input_genres:
    score *= 1.1  # 10% boost

score *= (1 + 0.1 * candidate.popularity_normalized)  # Up to 10% popularity boost
```

### 4. Recommendation Pipeline

1. Extract feature vectors for all input tracks
2. Compute mean feature vector (playlist profile)
3. Normalize profile to unit length
4. Find 1000 most similar tracks using KNN
5. Apply artist, genre, and popularity boosts
6. Sort by final score
7. Return top N recommendations

## Usage

```python
from recommender import Recommender

# Initialize recommender (loads and preprocesses data)
recommender = Recommender()

# Get recommendations
input_track_ids = ['track_id_1', 'track_id_2', 'track_id_3']
n_recommendations = 10
target_artist = {'Artist Name'}  # Optional hint

recommendations = recommender.get_recommendations(
    input_track_ids,
    n_recommendations,
    target_artist
)

# Returns: list of recommended track IDs, ordered by relevance
```

## Method Signature

```python
def get_recommendations(
    self,
    input_track_ids: list[str],
    n_recommendations: int,
    target_artist: set[str]
) -> list[str]:
    """
    Get recommendations based on multiple input songs

    Args:
        input_track_ids: List of track IDs to base recommendations on
        n_recommendations: Integer specifying how many songs to recommend
        target_artist: A set of artist names to boost in recommendations

    Returns:
        List of recommended track IDs of length n_recommendations
        The list is ordered by relevance (most relevant first)
    """
```

## Running Evaluation

To evaluate the recommender system:

```bash
python3 recommender.py
```

This will run the evaluation function (if `evaluation.py` is available) and print the results.

## Testing

Run the test scripts to see the recommender in action:

```bash
# Basic functionality test
python3 test_recommender.py

# Artist boosting test
python3 test_artist_boost2.py
```

## Requirements

- Python 3.7+
- pandas
- numpy
- scikit-learn

Install dependencies:
```bash
pip install pandas numpy scikit-learn
```

## Performance

- **Initialization time**: ~2-3 seconds (loads 89,740 tracks and builds KNN index)
- **Recommendation time**: ~0.1-0.2 seconds per query
- **Memory usage**: ~500MB for feature matrix and KNN index

## Future Improvements

1. **Advanced diversity**: Implement MMR (Maximal Marginal Relevance) for better genre/artist diversity
2. **Collaborative filtering**: Incorporate user listening history if available
3. **Temporal features**: Consider release date, trending score
4. **Approximate KNN**: Use FAISS or Annoy for faster search on larger datasets
5. **Weighted averaging**: Give more weight to recently played or highly rated input tracks
6. **Genre embeddings**: Learn genre relationships instead of exact matching
7. **Dynamic boosting**: Adjust boost strengths based on query characteristics
