# Testing Guide - Music Recommender System

Since you don't have access to `evaluation.py` yet, here are multiple ways to test and verify that your recommender system is working correctly.

## Quick Start - Run All Tests

```bash
# Comprehensive test suite (recommended)
python3 comprehensive_test.py

# Interactive demo with examples
python3 interactive_demo.py

# Simple functionality test
python3 test_recommender.py

# Artist boost verification
python3 test_artist_boost2.py
```

## Test Files Explained

### 1. `comprehensive_test.py` - Main Test Suite ⭐ RECOMMENDED

**What it tests:**
- ✅ Returns correct number of recommendations
- ✅ Returns unique track IDs (no duplicates)
- ✅ Excludes input tracks from recommendations
- ✅ Handles single and multiple input tracks
- ✅ Genre coherence (similar genres recommended)
- ✅ Artist boosting functionality
- ✅ Different recommendation sizes (1, 5, 10, 20, 50)
- ✅ Musical similarity (audio feature matching)
- ✅ Edge cases

**Expected output:**
```
TOTAL: 8/8 tests passed
🎉 All tests passed! The recommender system is working correctly.
```

### 2. `interactive_demo.py` - Visual Demonstrations

**What it shows:**
- Demo 1: Recommendations for popular songs
- Demo 2: Genre-specific recommendations (Jazz example)
- Demo 3: Mood-based recommendations (Happy/upbeat songs)
- Demo 4: Artist discovery with target_artist boost
- Demo 5: Custom search and recommendations

**Why use it:**
Shows real examples of how the recommender works with detailed song information including audio features.

### 3. `test_recommender.py` - Basic Functionality

Simple test that:
- Gets 3 acoustic songs
- Requests 5 recommendations
- Displays recommended songs with genre

### 4. `test_artist_boost2.py` - Artist Boost Verification

Tests the `target_artist` parameter:
- Gets recommendations WITHOUT artist boost
- Gets recommendations WITH artist boost
- Compares how many songs from target artist appear in each case

## Manual Testing - Using Python

You can manually test the recommender in Python:

```python
import pandas as pd
from recommender import Recommender

# Load data
df = pd.read_csv('dataset.csv')

# Initialize recommender
recommender = Recommender()

# Find some songs you like
rock_songs = df[df['track_genre'] == 'rock'].head(3)
print("Input songs:")
for _, song in rock_songs.iterrows():
    print(f"  - {song['track_name']} by {song['artists']}")

# Get recommendations
input_ids = rock_songs['track_id'].tolist()
recommendations = recommender.get_recommendations(
    input_track_ids=input_ids,
    n_recommendations=10,
    target_artist=set()  # or {'Artist Name'} to boost
)

# Display recommendations
print("\nRecommendations:")
for track_id in recommendations:
    track = df[df['track_id'] == track_id].iloc[0]
    print(f"  - {track['track_name']} by {track['artists']}")
```

## What to Look For

### ✅ Good Signs

1. **Consistency**: Running the same query twice should give identical results
2. **Relevance**: Recommended songs should match the vibe of input songs
3. **Genre coherence**: Most recommendations should be from similar genres
4. **Artist boost working**: More target artist songs when `target_artist` is set
5. **No duplicates**: Each recommendation should be unique
6. **No input songs**: Input songs should never appear in recommendations

### ❌ Red Flags

1. Random, unrelated recommendations
2. Duplicate track IDs in results
3. Wrong number of recommendations returned
4. Input tracks appearing in recommendations
5. Crashes or errors

## Verification Checklist

Before submitting to evaluation:

- [ ] Run `comprehensive_test.py` - all 8 tests pass
- [ ] Check recommendations make musical sense (similar genre/vibe)
- [ ] Verify artist boost increases target artist representation
- [ ] Test with different genres (rock, jazz, pop, etc.)
- [ ] Test with different input sizes (1, 3, 10, 20 songs)
- [ ] Test with different recommendation sizes (1, 10, 50)
- [ ] Verify no crashes or errors

## Performance Benchmarks

Expected performance on typical hardware:

- **Initialization**: 2-3 seconds
- **Single query**: 0.1-0.2 seconds
- **Memory usage**: ~500MB
- **Dataset size**: 89,740 unique tracks

## Common Issues and Solutions

### Issue: "ModuleNotFoundError: No module named 'pandas'"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: Warnings about divide by zero
**Solution**: These are internal sklearn warnings and don't affect functionality. They can be ignored or suppressed with:
```python
import warnings
warnings.filterwarnings('ignore')
```

### Issue: Slow initialization
**Solution**: Normal - building KNN index takes 2-3 seconds for 89K tracks

## Ready for Evaluation?

When you receive `evaluation.py`, simply run:

```bash
python3 recommender.py
```

The recommender is already configured to:
1. Initialize automatically
2. Load the dataset
3. Run evaluation
4. Print results

Your `get_recommendations()` method signature matches the evaluation requirements:
```python
def get_recommendations(
    self,
    input_track_ids: list[str],
    n_recommendations: int,
    target_artist: set[str]
) -> list[str]:
```

## Questions to Ask Yourself

1. ✅ Does it return the exact number of recommendations requested?
2. ✅ Are recommendations musically similar to input songs?
3. ✅ Does the artist boost actually work?
4. ✅ Can it handle edge cases (1 input song, 50 recommendations, etc.)?
5. ✅ Is it fast enough (<1 second per query)?

If you can answer YES to all of these, you're ready for evaluation!

## Next Steps

1. Run `comprehensive_test.py` to verify everything works
2. Explore `interactive_demo.py` to see recommendations in action
3. Optionally tune parameters (boost strengths, candidate pool size)
4. Wait for `evaluation.py` and run final evaluation
5. Submit your system!

Good luck! 🎵
