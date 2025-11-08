import pandas as pd
from recommender import Recommender
import warnings
warnings.filterwarnings('ignore')  # Suppress sklearn warnings for cleaner output

# Load dataset
df = pd.read_csv('dataset.csv')

# Get songs from multiple artists
test_songs = df[df['artists'].str.contains('Jason Mraz', na=False)].head(3)
print("Input songs:")
for _, row in test_songs.iterrows():
    print(f"  - {row['track_name']} by {row['artists']}")

input_track_ids = test_songs['track_id'].tolist()

# Create recommender
print("\nInitializing recommender...")
recommender = Recommender()

# Test 1: Without target artist
print("\n=== Test 1: Recommendations WITHOUT target artist boost ===")
recommendations_no_boost = recommender.get_recommendations(input_track_ids, 10, set())

for track_id in recommendations_no_boost:
    track = df[df['track_id'] == track_id].iloc[0]
    print(f"  - {track['track_name']} by {track['artists']}")

# Test 2: With target artist (boost Jason Mraz)
print("\n=== Test 2: Recommendations WITH target artist boost (Jason Mraz) ===")
target_artist = {'Jason Mraz'}
recommendations_with_boost = recommender.get_recommendations(input_track_ids, 10, target_artist)

for track_id in recommendations_with_boost:
    track = df[df['track_id'] == track_id].iloc[0]
    is_target = '***' if 'Jason Mraz' in track['artists'] else ''
    print(f"  - {track['track_name']} by {track['artists']} {is_target}")

print("\nNote: *** indicates songs by the target artist (Jason Mraz)")
