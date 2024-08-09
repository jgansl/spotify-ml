from dotenv import load_dotenv
from json import dump, dumps, load
from os import getenv, path
import spotipy
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import numpy as np

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
user_id = sp.me()['id']

# Function to get tracks from a playlist
def get_playlist_tracks(playlist_id):
    if playlist_id == 'saved':
        results = sp.current_user_saved_tracks()
    else:
        results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    # print(len(tracks))
    return tracks

# Function to get audio features in batches
def get_audio_features(track_ids):
    features_list = []
    for i in range(0, len(track_ids), 100):
        batch = track_ids[i:i+100]
        features = sp.audio_features(batch)
        features_list.extend(features)
    return pd.DataFrame(features_list)

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


# Get tracks from the playlist
# playlist_id = 'saved'
# tracks = get_playlist_tracks(playlist_id)
track_ids = []#[track['track']['id'] for track in tracks]
playlist_name = 'Cluster 1'#! assumes only one
playlist_id = get_playlist_id_by_name(user_id, playlist_name)
tracks = get_playlist_tracks(playlist_id)
track_ids.extend([track['track']['id'] for track in tracks])

# Get audio features
audio_features = get_audio_features(track_ids)

# Select features for clustering
features = audio_features[[
    #'danceability', 
    'energy', 
    #'loudness', 
    #'speechiness', 
    'acousticness', 
    #'instrumentalness', 
    #'liveness', 
    #'valence', 
    'tempo'
]]

# Standardize features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Perform DBSCAN clustering
dbscan = DBSCAN(eps=0.5, min_samples=5)  # You may need to tune these parameters
audio_features['cluster'] = dbscan.fit_predict(scaled_features)
#print(audio_features['cluster'].head(len(track_ids)))

# Filter out noise points (labeled as -1)
audio_features = audio_features[audio_features['cluster'] != -1]

# Get unique cluster labels
unique_clusters = audio_features['cluster'].unique()
print(f'Found {len(unique_clusters)} clusters.')

# Create new playlists based on clusters or update existing ones
for cluster in unique_clusters:
    cluster_tracks = audio_features[audio_features['cluster'] == cluster]['id'].tolist()
    playlist_name = f'Cluster 1 Cluster {cluster + 1}'
    
    # Check if the playlist already exists
    playlist_id = get_playlist_id_by_name(user_id, playlist_name)
    if playlist_id:
        # If it exists, replace the playlist contents
        sp.user_playlist_replace_tracks(user_id, playlist_id, cluster_tracks[:50])
        add_tracks_in_batches(user_id, playlist_id, cluster_tracks[50:])
    else:
        # If it doesn't exist, create a new playlist
        new_playlist = sp.user_playlist_create(user_id, playlist_name, public=False)
        add_tracks_in_batches(user_id, new_playlist['id'], cluster_tracks)

print("Playlists created or updated successfully.")