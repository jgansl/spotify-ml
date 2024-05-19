import pandas as pd
import numpy as np
import spotipy

from dotenv import load_dotenv
from json import dump, load
from os import getenv, path
from sklearn.cluster import DBSCAN,KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

# from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from spotipy.exceptions import SpotifyException



# Set up Spotify API credentials
load_dotenv()
# SPOTIPY_CLIENT_ID = getenv('SPOTIPY_CLIENT_ID')
# SPOTIPY_CLIENT_SECRET = getenv('SPOTIPY_CLIENT_SECRET')

# sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
#     client_id=SPOTIPY_CLIENT_ID,
#     client_secret=SPOTIPY_CLIENT_SECRET
# ))
usr = getenv('usr')

SCOPE = ",".join(
   [
   # Images
   "ugc-image-upload",
   # Listening History
   "user-read-recently-played",
   "user-read-playback-position",
   "user-top-read",
   # Playlists
   "playlist-modify-private",
   "playlist-read-collaborative",
   "playlist-read-private",
   "playlist-modify-public",
   # Playback
   "streaming",
   "app-remote-control",
   # Users
   "user-read-email",
   "user-read-private",
   # Follow
   "user-follow-read",
   "user-follow-modify",
   # Library
   "user-library-modify",
   "user-library-read",
   # Spotify Connect
   "user-read-currently-playing",
   "user-read-playback-state",
   "user-modify-playback-state",
   ]
)
auth = SpotifyOAuth(scope=SCOPE)#,open_browser=False, cache_path="./.cache.json")
sp   = Spotify(auth_manager=auth)


# Function to get tracks from a playlist
def get_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

# Function to get audio features
def get_audio_features(track_ids):
    features_list = []
    for i in range(0, len(track_ids), 100):
        batch = track_ids[i:i+100]
        features = sp.audio_features(batch)
        features_list.extend([f for f in features if f])
    return pd.DataFrame(features_list)

# Function to find the optimal number of clusters
def find_optimal_clusters(data, max_k):
    iters = range(2, max_k+1, 1)
    sse = []
    silhouette_scores = []

    for k in iters:
        kmeans = KMeans(n_clusters=k, random_state=42).fit(data)
        sse.append(kmeans.inertia_)
        score = silhouette_score(data, kmeans.labels_)
        silhouette_scores.append(score)

    return iters, sse, silhouette_scores

# Function to check if a playlist exists and return its ID
def get_playlist_id_by_name(user_id, playlist_name):
    playlists = sp.user_playlists(user_id)
    while playlists:
        for playlist in playlists['items']:
            if playlist['name'] == playlist_name:
                return playlist['id']
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
    return None

# Function to add tracks to a playlist in batches
def add_tracks_in_batches(user_id, playlist_id, track_ids):
    for i in range(0, len(track_ids), 50):
        batch = track_ids[i:i+50]
        sp.user_playlist_add_tracks(user_id, playlist_id, batch)
        sp.playlist_remove_all_occurrences_of_items(cache_playlist_id, batch)

# Get tracks from the playlist
filename = 'data/cache.json'
cache_playlist_id = '59XXAHeRlrTBZwyABUATRt' #cache
if path.exists(filename):
    with open(filename, 'r') as f:
        track_ids = load(f)
else:
    tracks = get_playlist_tracks(cache_playlist_id)
    track_ids = [track['track']['id'] for track in tracks]
    with open(filename, 'w') as f:
        dump(track_ids,f)
    input(f'Found: {len(track_ids)}')

track_ids = track_ids[:3000]

# Get audio features
audio_features = get_audio_features(track_ids)

# Select features for clustering
features = audio_features[
    [
        #'danceability', 
        'energy', 
        #'loudness', 
        #'speechiness', 
        'acousticness', 
        #'instrumentalness', 
        #'liveness', 
        #'valence', 
        'tempo'
    ]
]

# Standardize features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Find the optimal number of clusters
max_k = 10
iters, sse, silhouette_scores = find_optimal_clusters(scaled_features, max_k)

# Plot the Elbow Method and Silhouette Scores (optional)
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(iters, sse, '-o')
plt.xlabel('Number of clusters')
plt.ylabel('SSE')
plt.title('Elbow Method')

plt.subplot(1, 2, 2)
plt.plot(iters, silhouette_scores, '-o')
plt.xlabel('Number of clusters')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Scores')

plt.show()

# Choose the optimal number of clusters
optimal_k = iters[silhouette_scores.index(max(silhouette_scores))]

# Perform K-Means clustering
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
audio_features['cluster'] = kmeans.fit_predict(scaled_features)

# Create new playlists based on clusters
user_id = sp.me()['id']
# input('Destructive ')
# exit()
for cluster in range(optimal_k):
    cluster_tracks = audio_features[audio_features['cluster'] == cluster]['id'].tolist()
    playlist_name = f'Cluster {cluster + 13}' #! add cycle back in
    
    # Check if the playlist already exists
    playlist_id = get_playlist_id_by_name(user_id, playlist_name)
    if playlist_id: #! add tracks back in?
        # If it exists, replace the playlist contents
        sp.user_playlist_replace_tracks(user_id, playlist_id, cluster_tracks[:50])
        sp.playlist_remove_all_occurrences_of_items(cache_playlist_id, cluster_tracks[:50])
        add_tracks_in_batches(user_id, playlist_id, cluster_tracks[50:])
    else:
        # If it doesn't exist, create a new playlist
        new_playlist = sp.user_playlist_create(user_id, playlist_name, public=False)
        add_tracks_in_batches(user_id, new_playlist['id'], cluster_tracks)


print("Playlists created successfully.")
