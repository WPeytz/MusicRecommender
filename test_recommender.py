import pandas as pd
from recommender import Recommender

# Load dataset to get some sample track IDs
df = pd.read_csv('dataset.csv')

# Get 3 random acoustic songs
acoustic_songs = df[df['track_genre'] == 'acoustic'].head(3)
print("Input songs:")
for _, row in acoustic_songs.iterrows():
    print(f"  - {row['track_name']} by {row['artists']}")

input_track_ids = acoustic_songs['track_id'].tolist()

# Create recommender
print("\nInitializing recommender...")
recommender = Recommender()

# Get recommendations
print("\nGetting 5 recommendations...")
target_artist = set()  # Empty for this test
recommendations = recommender.get_recommendations(input_track_ids, 5, target_artist)

# Display recommendations
print("\nRecommended songs:")
for track_id in recommendations:
    track = df[df['track_id'] == track_id].iloc[0]
    print(f"  - {track['track_name']} by {track['artists']} (Genre: {track['track_genre']})")
