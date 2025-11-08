import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

class Recommender:

    def __init__(self):
        """Initialize the recommender by loading and preprocessing data"""
        print("Loading dataset...")
        # Load dataset
        self.df = pd.read_csv('dataset.csv')

        # Handle missing values
        self.df = self.df.dropna(subset=['artists', 'track_name'])

        # Remove duplicate track_ids (keep first occurrence)
        self.df = self.df.drop_duplicates(subset=['track_id'], keep='first')

        # Reset index to ensure continuous indexing
        self.df = self.df.reset_index(drop=True)

        print(f"Dataset loaded: {len(self.df)} unique tracks")

        # Define audio features to use for similarity
        self.audio_features = [
            'danceability', 'energy', 'valence', 'acousticness',
            'instrumentalness', 'speechiness', 'liveness',
            'loudness', 'tempo'
        ]

        # Normalize features that have different scales
        print("Normalizing features...")
        self.scaler_tempo = StandardScaler()
        self.scaler_loudness = StandardScaler()

        self.df['tempo_normalized'] = self.scaler_tempo.fit_transform(self.df[['tempo']])
        self.df['loudness_normalized'] = self.scaler_loudness.fit_transform(self.df[['loudness']])

        # Create feature matrix for similarity calculation
        self.feature_cols = [
            'danceability', 'energy', 'valence', 'acousticness',
            'instrumentalness', 'speechiness', 'liveness',
            'loudness_normalized', 'tempo_normalized'
        ]

        self.feature_matrix = self.df[self.feature_cols].values

        # Handle any remaining NaN or Inf values
        self.feature_matrix = np.nan_to_num(self.feature_matrix, nan=0.0, posinf=1.0, neginf=-1.0)

        # Normalize feature vectors to avoid issues with cosine distance
        # Add small epsilon to avoid division by zero
        norms = np.linalg.norm(self.feature_matrix, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1e-10, norms)  # Replace zero norms with small value
        self.feature_matrix = self.feature_matrix / norms

        # Build KNN model for efficient similarity search
        print("Building KNN index...")
        # Use min_neighbors to handle edge cases
        n_neighbors = min(500, len(self.df) - 1)
        self.knn_model = NearestNeighbors(n_neighbors=n_neighbors, metric='cosine', algorithm='brute')
        self.knn_model.fit(self.feature_matrix)

        # Create lookup dictionaries
        self.track_id_to_idx = {track_id: idx for idx, track_id in enumerate(self.df['track_id'])}
        self.idx_to_track_id = {idx: track_id for track_id, idx in self.track_id_to_idx.items()}

        # Parse artists into sets for matching
        self.df['artist_set'] = self.df['artists'].apply(
            lambda x: set(artist.strip() for artist in str(x).split(';'))
        )

        # Add popularity-normalized score for boosting
        self.df['popularity_score'] = self.df['popularity'] / 100.0

        print("Recommender initialized successfully!")

    def get_recommendations(self, input_track_ids: list[str], n_recommendations: int, target_artist: set[str]) -> list[str]:
        """
        Get recommendations based on multiple input songs

        Args:
            input_track_ids: List of track IDs to base recommendations on
            n_recommendations: Integer specifying how many songs to recommend
            target_artist: A set of artist names. This is a hint of which artists were removed from the playlist. You may use this set to recommend songs.

        Returns:
            List of recommended track IDs of length n_recommendations
            The list should be ordered by relevance (most relevant first)
        """

        # Get indices of input tracks
        input_indices = []
        for track_id in input_track_ids:
            if track_id in self.track_id_to_idx:
                input_indices.append(self.track_id_to_idx[track_id])

        if not input_indices:
            # Fallback: return most popular tracks
            return self.df.nlargest(n_recommendations, 'popularity')['track_id'].tolist()

        # Create aggregate feature vector from input tracks (using mean)
        input_features = self.feature_matrix[input_indices]
        target_profile = np.mean(input_features, axis=0).reshape(1, -1)

        # Normalize the target profile to match the normalized feature matrix
        profile_norm = np.linalg.norm(target_profile)
        if profile_norm > 0:
            target_profile = target_profile / profile_norm

        # Find candidate tracks using KNN
        # Use more candidates to ensure target_artist songs are in the pool
        n_candidates = min(max(n_recommendations * 20, 1000), len(self.df))
        distances, indices = self.knn_model.kneighbors(target_profile, n_neighbors=n_candidates)

        candidate_indices = indices[0]
        base_similarities = 1 - distances[0]  # Convert cosine distances to similarities

        # Get genres from input tracks
        input_genres = set(self.df.iloc[input_indices]['track_genre'].values)

        # Calculate final scores with various boosts
        scores = []
        for idx, base_sim in zip(candidate_indices, base_similarities):
            # Skip if it's an input track
            if idx in input_indices:
                continue

            track_row = self.df.iloc[idx]
            score = base_sim

            # Artist boost: if track is by a target artist, boost significantly
            if target_artist:
                artist_overlap = track_row['artist_set'].intersection(target_artist)
                if artist_overlap:
                    score *= 1.5  # 50% boost for target artists

            # Genre matching: boost if genre matches input tracks
            if track_row['track_genre'] in input_genres:
                score *= 1.1  # 10% boost for genre match

            # Popularity boost (slight preference for popular tracks)
            score *= (1 + 0.1 * track_row['popularity_score'])

            scores.append((idx, score))

        # Sort by score and get top N
        scores.sort(key=lambda x: x[1], reverse=True)
        top_indices = [idx for idx, _ in scores[:n_recommendations]]

        # Convert indices back to track IDs
        recommended_track_ids = [self.idx_to_track_id[idx] for idx in top_indices]

        return recommended_track_ids

# Only run evaluation when this file is executed directly
if __name__ == "__main__":
    try:
        from evaluation import evaluate
        recommender = Recommender()
        results = evaluate(recommender)
        print(results)
    except ImportError:
        print("Error: evaluation.py module not found")
        print("Please ensure evaluation.py is in the same directory")