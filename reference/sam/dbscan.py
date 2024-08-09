"""
Further Labeling of output playlists to describe
fine-tuning output as input
"""
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from sklearn.cluster import DBSCAN
import numpy as np

from spotipy.oauth2 import SpotifyOAuth
import sys, time

from _db import * # db, then external to spotify
from _functions import *
from _daily import privatizePlaylists
from random import shuffle

# # Set your Spotify API credentials
# SPOTIPY_CLIENT_ID = 'your_client_id'
# SPOTIPY_CLIENT_SECRET = 'your_client_secret'
# SPOTIPY_REDIRECT_URI = 'your_redirect_uri'
# SCOPE = 'playlist-modify-public playlist-modify-private playlist-read-private'

# # Authenticate with Spotify
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
#                                                client_secret=SPOTIPY_CLIENT_SECRET,
#                                                redirect_uri=SPOTIPY_REDIRECT_URI,
#                                                scope=SCOPE))

def get_playlist_tracks(playlist_name):
    user_playlists = sp.current_user_playlists()
    playlist = None

    while user_playlists:
        for item in user_playlists['items']:
            if item['name'] == playlist_name:
                playlist = item
                break
        if playlist:
            break
        if user_playlists['next']:
            user_playlists = sp.next(user_playlists)
        else:
            break

    if not playlist:
        print(f"No playlist found with the name: {playlist_name}")
        return None, None, None

    playlist_id = playlist['id']
    print(f"Fetching tracks from playlist: {playlist_name} (ID: {playlist_id})")

    tracks = []
    results = sp.playlist_tracks(playlist_id)
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    track_ids = [track['track']['id'] for track in tracks]
    return playlist_id, track_ids, playlist_name

def get_audio_features(track_ids):
    features = []
    for i in range(0, len(track_ids), 100):
        audio_features = sp.audio_features(track_ids[i:i+100])
        features.extend(audio_features)
    return features

def cluster_tracks(track_features):
    feature_matrix = np.array([[f['danceability'], f['energy'], f['tempo'], f['valence']] for f in track_features if f is not None])
    dbscan = DBSCAN(eps=0.5, min_samples=5).fit(feature_matrix)
    return dbscan.labels_

def find_or_create_playlist(playlist_name):
    user_playlists = sp.current_user_playlists()
    playlist_id = None

    while user_playlists:
        for item in user_playlists['items']:
            if item['name'] == playlist_name:
                playlist_id = item['id']
                break
        if playlist_id:
            break
        if user_playlists['next']:
            user_playlists = sp.next(user_playlists)
        else:
            break

    if not playlist_id:
        new_playlist = sp.user_playlist_create(sp.me()['id'], playlist_name)
        playlist_id = new_playlist['id']
    else:
        sp.playlist_replace_items(playlist_id, [])  # Clear the existing playlist

    return playlist_id

def create_clustered_playlists(original_playlist_name, track_ids, clusters):
    cluster_dict = {}
    for track_id, cluster in zip(track_ids, clusters):
        if cluster not in cluster_dict:
            cluster_dict[cluster] = []
        cluster_dict[cluster].append(track_id)

    for cluster, ids in cluster_dict.items():
        if cluster == -1:
            new_playlist_name = f"Noise - {original_playlist_name}"
        else:
            new_playlist_name = f"Cluster {cluster + 1} - {original_playlist_name}"
        
        new_playlist_id = find_or_create_playlist(new_playlist_name)

        # Add tracks to the new playlist in batches of 100
        for i in range(0, len(ids), 100):
            sp.playlist_add_items(new_playlist_id, ids[i:i+100])

        print(f"Created or updated playlist: {new_playlist_name} with {len(ids)} tracks")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        playlist_name = " ".join(sys.argv[1:])
        playlist_id, track_ids, original_playlist_name = get_playlist_tracks(playlist_name)
        if playlist_id and track_ids:
            track_features = get_audio_features(track_ids)
            clusters = cluster_tracks(track_features)
            create_clustered_playlists(original_playlist_name, track_ids, clusters)
    else:
        print("Please provide a playlist name as an argument.")
