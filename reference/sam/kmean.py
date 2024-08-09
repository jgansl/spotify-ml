import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys, time

from _db import * # db, then external to spotify
from _functions import *
from _daily import privatizePlaylists
from random import shuffle

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
        return None, None

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

def cluster_tracks(track_features, num_clusters):
    feature_matrix = np.array([[f['danceability'], f['energy'], f['tempo'], f['valence']] for f in track_features if f is not None])
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(feature_matrix)
    return kmeans.labels_

def create_clustered_playlists(original_playlist_name, track_ids, clusters):
    cluster_dict = {}
    for track_id, cluster in zip(track_ids, clusters):
        if cluster not in cluster_dict:
            cluster_dict[cluster] = []
        cluster_dict[cluster].append(track_id)

    for cluster, ids in cluster_dict.items():
        new_playlist_name = f"{original_playlist_name} - Cluster {cluster + 1}"
        new_playlist = sp.user_playlist_create(sp.me()['id'], new_playlist_name)
        new_playlist_id = new_playlist['id']

        # Add tracks to the new playlist in batches of 100
        for i in range(0, len(ids), 100):
            sp.playlist_add_items(new_playlist_id, ids[i:i+100])

        print(f"Created playlist: {new_playlist_name} with {len(ids)} tracks")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        playlist_name = " ".join(sys.argv[1:])
        playlist_id, track_ids, original_playlist_name = get_playlist_tracks(playlist_name)
        if playlist_id and track_ids:
            track_features = get_audio_features(track_ids)
            num_clusters = 3  # You can change the number of clusters as needed
            clusters = cluster_tracks(track_features, num_clusters)
            create_clustered_playlists(original_playlist_name, track_ids, clusters)
    else:
        print("Please provide a playlist name as an argument.")