"""
Interactive Demo - Explore recommendations for different songs
"""

import pandas as pd
from recommender import Recommender
import warnings
warnings.filterwarnings('ignore')

def print_separator():
    print("\n" + "="*80)

def search_songs(df, keyword, limit=10):
    """Search for songs by name or artist"""
    keyword_lower = keyword.lower()
    matches = df[
        df['track_name'].str.lower().str.contains(keyword_lower, na=False) |
        df['artists'].str.lower().str.contains(keyword_lower, na=False)
    ].head(limit)
    return matches

def display_song_details(track, index=None):
    """Display detailed song information"""
    prefix = f"{index}. " if index else "  "
    print(f"{prefix}{track['track_name']}")
    print(f"   Artist: {track['artists']}")
    print(f"   Genre: {track['track_genre']}, Popularity: {track['popularity']}")
    print(f"   Features: dance={track['danceability']:.2f}, energy={track['energy']:.2f}, "
          f"valence={track['valence']:.2f}, acoustic={track['acousticness']:.2f}")
    print(f"   Track ID: {track['track_id']}")

def demo_1_popular_songs(recommender, df):
    """Demo 1: Recommendations for popular songs"""
    print_separator()
    print("DEMO 1: Recommendations for Popular Songs")
    print_separator()

    # Get top popular songs from different genres
    popular = df.nlargest(100, 'popularity')
    test_songs = popular.sample(3, random_state=42)

    print("\n📀 INPUT SONGS:")
    for i, (_, song) in enumerate(test_songs.iterrows(), 1):
        display_song_details(song, i)

    input_ids = test_songs['track_id'].tolist()
    recommendations = recommender.get_recommendations(input_ids, 10, set())

    print("\n🎵 RECOMMENDATIONS:")
    for i, track_id in enumerate(recommendations, 1):
        track = df[df['track_id'] == track_id].iloc[0]
        display_song_details(track, i)

def demo_2_genre_specific(recommender, df):
    """Demo 2: Genre-specific recommendations"""
    print_separator()
    print("DEMO 2: Genre-Specific Recommendations (Jazz)")
    print_separator()

    jazz_songs = df[df['track_genre'] == 'jazz'].head(3)

    print("\n🎷 INPUT SONGS (Jazz):")
    for i, (_, song) in enumerate(jazz_songs.iterrows(), 1):
        display_song_details(song, i)

    input_ids = jazz_songs['track_id'].tolist()
    recommendations = recommender.get_recommendations(input_ids, 10, set())

    print("\n🎵 RECOMMENDATIONS:")
    genre_counts = {}
    for i, track_id in enumerate(recommendations, 1):
        track = df[df['track_id'] == track_id].iloc[0]
        genre = track['track_genre']
        genre_counts[genre] = genre_counts.get(genre, 0) + 1
        genre_marker = " ✓ JAZZ" if genre == 'jazz' else f" ({genre})"
        print(f"{i}. {track['track_name']} by {track['artists']}{genre_marker}")

    print(f"\nGenre distribution: {dict(genre_counts)}")

def demo_3_mood_based(recommender, df):
    """Demo 3: Mood-based recommendations (Happy songs)"""
    print_separator()
    print("DEMO 3: Mood-Based Recommendations (Happy/Upbeat)")
    print_separator()

    # High valence = happy songs
    happy_songs = df[(df['valence'] > 0.8) & (df['energy'] > 0.7)].head(3)

    print("\n😊 INPUT SONGS (High valence & energy = happy/upbeat):")
    for i, (_, song) in enumerate(happy_songs.iterrows(), 1):
        display_song_details(song, i)

    input_ids = happy_songs['track_id'].tolist()
    recommendations = recommender.get_recommendations(input_ids, 10, set())

    print("\n🎵 RECOMMENDATIONS:")
    total_valence = 0
    total_energy = 0
    for i, track_id in enumerate(recommendations, 1):
        track = df[df['track_id'] == track_id].iloc[0]
        total_valence += track['valence']
        total_energy += track['energy']
        mood = "😊" if track['valence'] > 0.7 else "😐"
        print(f"{i}. {track['track_name']} by {track['artists']}")
        print(f"    valence={track['valence']:.2f}, energy={track['energy']:.2f} {mood}")

    avg_valence = total_valence / 10
    avg_energy = total_energy / 10
    print(f"\nAverage valence: {avg_valence:.2f} (input avg: {happy_songs['valence'].mean():.2f})")
    print(f"Average energy: {avg_energy:.2f} (input avg: {happy_songs['energy'].mean():.2f})")

def demo_4_artist_discovery(recommender, df):
    """Demo 4: Artist discovery with target artist"""
    print_separator()
    print("DEMO 4: Artist Discovery (with target_artist hint)")
    print_separator()

    # Get some indie songs
    indie_songs = df[df['track_genre'] == 'indie'].head(3)

    # Find a popular indie artist to target
    indie_artists = df[df['track_genre'] == 'indie']['artists'].str.split(';').explode()
    common_indie_artists = indie_artists.value_counts().head(10)
    target = common_indie_artists.index[0]

    print(f"\n🎸 INPUT SONGS (Indie genre):")
    for i, (_, song) in enumerate(indie_songs.iterrows(), 1):
        display_song_details(song, i)

    print(f"\n🎯 TARGET ARTIST: {target}")
    print("(This artist hint will boost their songs in recommendations)")

    input_ids = indie_songs['track_id'].tolist()

    # Without boost
    print("\n🎵 RECOMMENDATIONS WITHOUT ARTIST BOOST:")
    recs_no_boost = recommender.get_recommendations(input_ids, 10, set())
    no_boost_count = 0
    for i, track_id in enumerate(recs_no_boost, 1):
        track = df[df['track_id'] == track_id].iloc[0]
        if target in track['artists']:
            no_boost_count += 1
            print(f"{i}. {track['track_name']} by {track['artists']} ⭐")
        else:
            print(f"{i}. {track['track_name']} by {track['artists']}")

    # With boost
    print(f"\n🎵 RECOMMENDATIONS WITH ARTIST BOOST (targeting {target}):")
    recs_with_boost = recommender.get_recommendations(input_ids, 10, {target})
    with_boost_count = 0
    for i, track_id in enumerate(recs_with_boost, 1):
        track = df[df['track_id'] == track_id].iloc[0]
        if target in track['artists']:
            with_boost_count += 1
            print(f"{i}. {track['track_name']} by {track['artists']} ⭐ BOOSTED")
        else:
            print(f"{i}. {track['track_name']} by {track['artists']}")

    print(f"\nTarget artist songs WITHOUT boost: {no_boost_count}/10")
    print(f"Target artist songs WITH boost: {with_boost_count}/10")

def demo_5_custom_search(recommender, df):
    """Demo 5: Custom search and recommendations"""
    print_separator()
    print("DEMO 5: Custom Search - Find and Recommend")
    print_separator()

    print("\nLet's search for songs and get recommendations!")
    print("\nSearching for songs with 'love' in title or artist...")

    matches = search_songs(df, 'love', limit=5)

    print("\nFound songs:")
    for i, (_, song) in enumerate(matches.iterrows(), 1):
        display_song_details(song, i)

    if len(matches) >= 2:
        # Use first 2 matches
        input_ids = matches.head(2)['track_id'].tolist()

        print("\n🎵 RECOMMENDATIONS based on first 2 songs:")
        recommendations = recommender.get_recommendations(input_ids, 10, set())

        for i, track_id in enumerate(recommendations, 1):
            track = df[df['track_id'] == track_id].iloc[0]
            print(f"{i}. {track['track_name']} by {track['artists']} [{track['track_genre']}]")

def main():
    """Run all demos"""
    print("\n" + "█"*80)
    print("  MUSIC RECOMMENDER SYSTEM - INTERACTIVE DEMO")
    print("█"*80)

    print("\nInitializing recommender system...")
    df = pd.read_csv('dataset.csv')
    recommender = Recommender()

    print("\n✓ Recommender ready!")
    print(f"✓ {len(df)} total tracks in database")
    print(f"✓ {df['track_genre'].nunique()} genres available")

    # Run demos
    demo_1_popular_songs(recommender, df)
    demo_2_genre_specific(recommender, df)
    demo_3_mood_based(recommender, df)
    demo_4_artist_discovery(recommender, df)
    demo_5_custom_search(recommender, df)

    print_separator()
    print("🎉 Demo complete! The recommender system is working correctly.")
    print("\nYou can use the Recommender class in your own code:")
    print("  from recommender import Recommender")
    print("  recommender = Recommender()")
    print("  recs = recommender.get_recommendations(track_ids, n, target_artist)")
    print_separator()

if __name__ == "__main__":
    main()
