import pandas as pd
from recommender import Recommender
import warnings
warnings.filterwarnings('ignore')

# Load dataset
df = pd.read_csv('dataset.csv')

# Get pop songs (NOT by The Weeknd)
test_songs = df[(df['track_genre'] == 'pop') & (~df['artists'].str.contains('The Weeknd', na=False))].head(3)
print("Input songs (Pop genre, NOT by The Weeknd):")
for _, row in test_songs.iterrows():
    print(f"  - {row['track_name']} by {row['artists']}")

input_track_ids = test_songs['track_id'].tolist()

# Create recommender
print("\nInitializing recommender...")
recommender = Recommender()

# Test 1: Without target artist
print("\n=== Test 1: Top 10 recommendations WITHOUT target artist ===")
recommendations_no_boost = recommender.get_recommendations(input_track_ids, 10, set())

weeknd_count_no_boost = 0
for track_id in recommendations_no_boost:
    track = df[df['track_id'] == track_id].iloc[0]
    is_weeknd = ' *** The Weeknd' if 'The Weeknd' in track['artists'] else ''
    if 'The Weeknd' in track['artists']:
        weeknd_count_no_boost += 1
    print(f"  - {track['track_name']} by {track['artists']}{is_weeknd}")

# Test 2: With target artist (boost The Weeknd)
print("\n=== Test 2: Top 10 recommendations WITH target artist boost (The Weeknd) ===")
target_artist = {'The Weeknd'}
recommendations_with_boost = recommender.get_recommendations(input_track_ids, 10, target_artist)

weeknd_count_with_boost = 0
for track_id in recommendations_with_boost:
    track = df[df['track_id'] == track_id].iloc[0]
    is_weeknd = ' *** The Weeknd' if 'The Weeknd' in track['artists'] else ''
    if 'The Weeknd' in track['artists']:
        weeknd_count_with_boost += 1
    print(f"  - {track['track_name']} by {track['artists']}{is_weeknd}")

print(f"\nThe Weeknd songs WITHOUT boost: {weeknd_count_no_boost}/10")
print(f"The Weeknd songs WITH boost: {weeknd_count_with_boost}/10")
