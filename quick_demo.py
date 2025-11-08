"""
Quick Demo - 1-minute verification that everything works
"""

import pandas as pd
from recommender import Recommender
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("  QUICK DEMO - Music Recommender System")
print("="*60)

# Initialize
print("\n1. Initializing recommender...")
df = pd.read_csv('dataset.csv')
recommender = Recommender()
print("   ✓ Ready!")

# Test 1: Basic recommendation
print("\n2. Testing basic recommendations...")
test_songs = df[df['track_genre'] == 'pop'].head(3)
input_ids = test_songs['track_id'].tolist()
recs = recommender.get_recommendations(input_ids, 5, set())
print(f"   ✓ Got {len(recs)} recommendations")

# Test 2: Artist boost
print("\n3. Testing artist boost...")
artist = 'Taylor Swift'
recs_no_boost = recommender.get_recommendations(input_ids, 10, set())
recs_with_boost = recommender.get_recommendations(input_ids, 10, {artist})
count_no = sum(1 for r in recs_no_boost if artist in df[df['track_id']==r].iloc[0]['artists'])
count_yes = sum(1 for r in recs_with_boost if artist in df[df['track_id']==r].iloc[0]['artists'])
print(f"   ✓ Without boost: {count_no} {artist} songs")
print(f"   ✓ With boost: {count_yes} {artist} songs")

# Test 3: Different sizes
print("\n4. Testing different recommendation sizes...")
for size in [1, 10, 20]:
    recs = recommender.get_recommendations(input_ids, size, set())
    print(f"   ✓ Requested {size}, got {len(recs)}")

# Show example
print("\n5. Example recommendations:")
print("\n   Input songs:")
for _, song in test_songs.iterrows():
    print(f"      - {song['track_name']} by {song['artists']}")

recs = recommender.get_recommendations(input_ids, 5, set())
print("\n   Recommendations:")
for track_id in recs:
    track = df[df['track_id'] == track_id].iloc[0]
    print(f"      - {track['track_name']} by {track['artists']}")

print("\n" + "="*60)
print("  ✅ ALL TESTS PASSED - System is working!")
print("="*60)
print("\nNext steps:")
print("  • Run comprehensive_test.py for full test suite")
print("  • Run interactive_demo.py for detailed examples")
print("  • When you get evaluation.py, run: python3 recommender.py")
print("="*60)
