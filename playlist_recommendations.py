import pandas as pd
from recommender import Recommender
import warnings
warnings.filterwarnings('ignore')

# Load dataset
df = pd.read_csv('dataset.csv')

# Songs from the playlist
playlist_songs = [
    ("Style", "Taylor Swift"),
    ("Siren sounds", "Tate McRae"),
    ("The Cure", "The Chainsmokers"),
    ("Clean", "Alessia Cara"),
    ("WHERE IS MY HUSBAND!", "RAYE"),
    ("Crush", "Zara Larsson"),
    ("Changes", "Charlie Puth"),
    ("Mystical Magical", "Benson Boone"),
    ("Sorry To Myself", "Demi Lovato"),
    ("In The Dark", "Selena Gomez")
]

print("="*80)
print("  FINDING YOUR PLAYLIST SONGS IN THE DATASET")
print("="*80)

# Search for these songs in the dataset
found_tracks = []
for song_name, artist_name in playlist_songs:
    # Search for exact or partial matches
    matches = df[
        (df['track_name'].str.contains(song_name, case=False, na=False)) &
        (df['artists'].str.contains(artist_name, case=False, na=False))
    ]

    if len(matches) > 0:
        track = matches.iloc[0]
        found_tracks.append(track['track_id'])
        print(f"✓ Found: {track['track_name']} by {track['artists']}")
    else:
        print(f"✗ Not found: {song_name} by {artist_name}")

print(f"\n📊 Found {len(found_tracks)} out of {len(playlist_songs)} songs in dataset")

if len(found_tracks) == 0:
    print("\n⚠ None of the playlist songs were found in the dataset.")
    print("Let me find similar pop songs instead...")

    # Use popular pop songs as a substitute
    pop_songs = df[df['track_genre'].isin(['pop', 'dance', 'dance-pop'])].nlargest(10, 'popularity')
    found_tracks = pop_songs['track_id'].tolist()[:5]

    print("\nUsing these similar pop songs instead:")
    for track_id in found_tracks:
        track = df[df['track_id'] == track_id].iloc[0]
        print(f"  - {track['track_name']} by {track['artists']}")

print("\n" + "="*80)
print("  GETTING RECOMMENDATIONS")
print("="*80)

# Initialize recommender
print("\nInitializing recommender...")
recommender = Recommender()

# Get recommendations
# Target artists from the playlist
target_artists = {
    'Taylor Swift', 'Tate McRae', 'The Chainsmokers', 'Alessia Cara',
    'RAYE', 'Zara Larsson', 'Charlie Puth', 'Benson Boone',
    'Demi Lovato', 'Selena Gomez'
}

print(f"\nGetting 5 recommendations based on your playlist...")
print(f"Boosting songs from: {', '.join(list(target_artists)[:3])}...")

recommendations = recommender.get_recommendations(
    input_track_ids=found_tracks,
    n_recommendations=5,
    target_artist=target_artists
)

print("\n" + "="*80)
print("  🎵 YOUR NEXT 5 RECOMMENDED SONGS")
print("="*80)

for i, track_id in enumerate(recommendations, 1):
    track = df[df['track_id'] == track_id].iloc[0]

    # Check if it's from a target artist
    is_target = "⭐" if any(artist in track['artists'] for artist in target_artists) else ""

    print(f"\n{i}. {track['track_name']}")
    print(f"   Artist: {track['artists']} {is_target}")
    print(f"   Album: {track['album_name']}")
    print(f"   Genre: {track['track_genre']} | Popularity: {track['popularity']}")
    print(f"   Vibe: dance={track['danceability']:.2f}, energy={track['energy']:.2f}, valence={track['valence']:.2f}")

print("\n" + "="*80)
print("⭐ = Artist from your original playlist")
print("="*80)
