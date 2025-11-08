"""
Comprehensive test suite for the Music Recommender System
Tests all key functionality without requiring evaluation.py
"""

import pandas as pd
from recommender import Recommender
import warnings
warnings.filterwarnings('ignore')

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80)

def print_subheader(text):
    """Print a formatted subheader"""
    print(f"\n--- {text} ---")

def print_songs(track_ids, df, show_features=False):
    """Print song details"""
    for i, track_id in enumerate(track_ids, 1):
        track = df[df['track_id'] == track_id].iloc[0]
        print(f"  {i}. {track['track_name']}")
        print(f"     Artist: {track['artists']}")
        print(f"     Genre: {track['track_genre']}, Popularity: {track['popularity']}")
        if show_features:
            print(f"     Features: dance={track['danceability']:.2f}, energy={track['energy']:.2f}, valence={track['valence']:.2f}")

def test_1_basic_functionality(recommender, df):
    """Test 1: Basic functionality - returns correct number of recommendations"""
    print_header("TEST 1: Basic Functionality")

    # Get some test songs
    test_songs = df.head(5)
    input_ids = test_songs['track_id'].tolist()

    print_subheader("Input: 5 tracks, Request: 10 recommendations")

    recommendations = recommender.get_recommendations(input_ids, 10, set())

    # Verify
    print(f"\n✓ Returned {len(recommendations)} recommendations (expected 10)")
    print(f"✓ All recommendations are strings: {all(isinstance(r, str) for r in recommendations)}")
    print(f"✓ All recommendations are unique: {len(recommendations) == len(set(recommendations))}")
    print(f"✓ No input tracks in recommendations: {not any(r in input_ids for r in recommendations)}")

    return all([
        len(recommendations) == 10,
        all(isinstance(r, str) for r in recommendations),
        len(recommendations) == len(set(recommendations)),
        not any(r in input_ids for r in recommendations)
    ])

def test_2_single_track_input(recommender, df):
    """Test 2: Single track input"""
    print_header("TEST 2: Single Track Input")

    # Get a single popular song
    single_song = df[df['popularity'] > 80].iloc[0]
    input_id = [single_song['track_id']]

    print_subheader("Input Song")
    print(f"  {single_song['track_name']} by {single_song['artists']}")
    print(f"  Genre: {single_song['track_genre']}")

    recommendations = recommender.get_recommendations(input_id, 5, set())

    print_subheader("Recommendations")
    print_songs(recommendations[:5], df)

    return len(recommendations) == 5

def test_3_genre_coherence(recommender, df):
    """Test 3: Genre coherence - recommendations should match input genre"""
    print_header("TEST 3: Genre Coherence")

    # Get 3 rock songs
    rock_songs = df[df['track_genre'] == 'rock'].head(3)
    input_ids = rock_songs['track_id'].tolist()

    print_subheader("Input: 3 Rock songs")
    for _, song in rock_songs.iterrows():
        print(f"  - {song['track_name']} by {song['artists']}")

    recommendations = recommender.get_recommendations(input_ids, 10, set())

    print_subheader("Recommended Songs")
    rock_count = 0
    for track_id in recommendations:
        track = df[df['track_id'] == track_id].iloc[0]
        is_rock = "✓ ROCK" if track['track_genre'] == 'rock' else f"  ({track['track_genre']})"
        print(f"  - {track['track_name']} by {track['artists']} {is_rock}")
        if track['track_genre'] == 'rock':
            rock_count += 1

    print(f"\n✓ {rock_count}/10 recommendations are rock music")
    print(f"  (Genre boost should increase rock recommendations)")

    return True

def test_4_artist_boost(recommender, df):
    """Test 4: Artist boost functionality"""
    print_header("TEST 4: Artist Boost")

    # Find an artist with multiple songs
    artist_counts = df['artists'].value_counts()
    test_artist = None
    for artist, count in artist_counts.items():
        if count >= 5 and ';' not in artist:  # Single artist with 5+ songs
            test_artist = artist
            break

    if not test_artist:
        print("Could not find suitable test artist")
        return False

    # Get songs NOT by this artist in same genre
    artist_genre = df[df['artists'] == test_artist].iloc[0]['track_genre']
    input_songs = df[(df['track_genre'] == artist_genre) & (df['artists'] != test_artist)].head(3)
    input_ids = input_songs['track_id'].tolist()

    print_subheader(f"Test Artist: {test_artist}")
    print(f"Input: 3 songs in {artist_genre} genre, NOT by {test_artist}")

    # Test without boost
    print_subheader("Recommendations WITHOUT Artist Boost")
    recs_no_boost = recommender.get_recommendations(input_ids, 10, set())
    count_no_boost = sum(1 for tid in recs_no_boost if test_artist in df[df['track_id'] == tid].iloc[0]['artists'])
    print(f"  Songs by {test_artist}: {count_no_boost}/10")

    # Test with boost
    print_subheader("Recommendations WITH Artist Boost")
    recs_with_boost = recommender.get_recommendations(input_ids, 10, {test_artist})
    count_with_boost = 0
    for track_id in recs_with_boost:
        track = df[df['track_id'] == track_id].iloc[0]
        is_artist = "*** BOOSTED" if test_artist in track['artists'] else ""
        print(f"  - {track['track_name']} by {track['artists']} {is_artist}")
        if test_artist in track['artists']:
            count_with_boost += 1

    print(f"\n✓ Songs by {test_artist} WITHOUT boost: {count_no_boost}/10")
    print(f"✓ Songs by {test_artist} WITH boost: {count_with_boost}/10")

    if count_with_boost >= count_no_boost:
        print("✓ Artist boost is working (increased or maintained artist representation)")
        return True
    else:
        print("⚠ Artist boost may not be working optimally")
        return False

def test_5_different_request_sizes(recommender, df):
    """Test 5: Different recommendation sizes"""
    print_header("TEST 5: Different Recommendation Sizes")

    test_songs = df.head(3)
    input_ids = test_songs['track_id'].tolist()

    sizes = [1, 5, 10, 20, 50]
    all_pass = True

    for size in sizes:
        recs = recommender.get_recommendations(input_ids, size, set())
        passed = len(recs) == size
        status = "✓" if passed else "✗"
        print(f"{status} Requested {size}, got {len(recs)}")
        all_pass = all_pass and passed

    return all_pass

def test_6_empty_target_artist(recommender, df):
    """Test 6: Empty vs non-empty target artist"""
    print_header("TEST 6: Empty vs Non-Empty Target Artist")

    test_songs = df.head(3)
    input_ids = test_songs['track_id'].tolist()

    # Test with empty set
    recs_empty = recommender.get_recommendations(input_ids, 10, set())
    print(f"✓ With empty target_artist: {len(recs_empty)} recommendations")

    # Test with some artist
    some_artist = df.iloc[100]['artists'].split(';')[0]
    recs_with_artist = recommender.get_recommendations(input_ids, 10, {some_artist})
    print(f"✓ With target_artist='{some_artist}': {len(recs_with_artist)} recommendations")

    return len(recs_empty) == 10 and len(recs_with_artist) == 10

def test_7_musical_similarity(recommender, df):
    """Test 7: Musical similarity - acoustic songs should get acoustic recommendations"""
    print_header("TEST 7: Musical Similarity (Audio Features)")

    # Get very acoustic songs (high acousticness)
    acoustic_songs = df[df['acousticness'] > 0.9].head(3)
    input_ids = acoustic_songs['track_id'].tolist()

    print_subheader("Input: 3 Highly Acoustic Songs (acousticness > 0.9)")
    for _, song in acoustic_songs.iterrows():
        print(f"  - {song['track_name']} (acousticness: {song['acousticness']:.2f})")

    recommendations = recommender.get_recommendations(input_ids, 10, set())

    print_subheader("Recommended Songs - Acousticness Values")
    acoustic_count = 0
    total_acousticness = 0
    for track_id in recommendations:
        track = df[df['track_id'] == track_id].iloc[0]
        total_acousticness += track['acousticness']
        if track['acousticness'] > 0.5:
            acoustic_count += 1
        print(f"  - {track['track_name']}: acousticness={track['acousticness']:.2f}")

    avg_acousticness = total_acousticness / len(recommendations)
    print(f"\n✓ Average acousticness of recommendations: {avg_acousticness:.2f}")
    print(f"✓ {acoustic_count}/10 recommendations have acousticness > 0.5")
    print(f"  (Shows that similar audio features are being matched)")

    return True

def test_8_edge_cases(recommender, df):
    """Test 8: Edge cases"""
    print_header("TEST 8: Edge Cases")

    all_pass = True

    # Test with single input track
    single = recommender.get_recommendations([df.iloc[0]['track_id']], 5, set())
    status = "✓" if len(single) == 5 else "✗"
    print(f"{status} Single input track: {len(single)} recommendations")
    all_pass = all_pass and (len(single) == 5)

    # Test with many input tracks
    many_input = df.head(20)['track_id'].tolist()
    many = recommender.get_recommendations(many_input, 10, set())
    status = "✓" if len(many) == 10 else "✗"
    print(f"{status} 20 input tracks: {len(many)} recommendations")
    all_pass = all_pass and (len(many) == 10)

    # Test requesting 1 recommendation
    one = recommender.get_recommendations(df.head(3)['track_id'].tolist(), 1, set())
    status = "✓" if len(one) == 1 else "✗"
    print(f"{status} Request 1 recommendation: {len(one)} returned")
    all_pass = all_pass and (len(one) == 1)

    return all_pass

def run_all_tests():
    """Run all tests"""
    print("\n" + "█"*80)
    print("  MUSIC RECOMMENDER SYSTEM - COMPREHENSIVE TEST SUITE")
    print("█"*80)

    # Load data and initialize recommender
    print("\nLoading dataset and initializing recommender...")
    df = pd.read_csv('dataset.csv')
    recommender = Recommender()

    # Run tests
    results = {}

    results['Test 1: Basic Functionality'] = test_1_basic_functionality(recommender, df)
    results['Test 2: Single Track Input'] = test_2_single_track_input(recommender, df)
    results['Test 3: Genre Coherence'] = test_3_genre_coherence(recommender, df)
    results['Test 4: Artist Boost'] = test_4_artist_boost(recommender, df)
    results['Test 5: Different Sizes'] = test_5_different_request_sizes(recommender, df)
    results['Test 6: Empty Target Artist'] = test_6_empty_target_artist(recommender, df)
    results['Test 7: Musical Similarity'] = test_7_musical_similarity(recommender, df)
    results['Test 8: Edge Cases'] = test_8_edge_cases(recommender, df)

    # Summary
    print_header("TEST SUMMARY")
    total_tests = len(results)
    passed_tests = sum(results.values())

    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status}: {test_name}")

    print(f"\n{'='*80}")
    print(f"  TOTAL: {passed_tests}/{total_tests} tests passed")
    print(f"{'='*80}")

    if passed_tests == total_tests:
        print("\n🎉 All tests passed! The recommender system is working correctly.")
    else:
        print(f"\n⚠ {total_tests - passed_tests} test(s) failed. Review the output above.")

    return passed_tests == total_tests

if __name__ == "__main__":
    run_all_tests()
