"""
backup original playlist
"""
import spotipy
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
# SCOPE = 'playlist-modify-public playlist-modify-private'

# # Authenticate with Spotify
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
#                                                client_secret=SPOTIPY_CLIENT_SECRET,
#                                                redirect_uri=SPOTIPY_REDIRECT_URI,
#                                                scope=SCOPE))

def new_get_playlist_tracks(playlist_name):
    # Get the current user's playlists
    user_playlists = sp.current_user_playlists()
    playlist = None

    # Iterate through the playlists to find the one with the given name
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

    # Fetch all tracks from the playlist
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    # Extract release dates and sort tracks
    sorted_tracks = sorted(tracks, key=lambda x: sp.track(x['track']['id'])['album']['release_date'])

    # Get track URIs in sorted order
    sorted_track_uris = [track['track']['uri'] for track in sorted_tracks]

    return playlist_id, sorted_track_uris

def reorder_playlist(playlist_id, sorted_track_uris):
    try:
        # Clear the playlist first
        sp.playlist_replace_items(playlist_id, [])
        
        # Add tracks one at a time with a 0.1 second throttle
        for track_uri in sorted_track_uris:
            sp.playlist_add_items(playlist_id, [track_uri])
            time.sleep(0.25)
        
        print(f"Reordered playlist with ID: {playlist_id}")
    except spotipy.exceptions.SpotifyException as e:
        print(f"An error occurred: {e}")
        if e.http_status == 404:
            print("The playlist could not be found. Please check the playlist ID and permissions.")

if __name__ == "__main__":
   #  if len(sys.argv) > 1:
   #      playlist_name = " ".join(sys.argv[1:])
   for i in [
      'Chill',
      'Dance/Electronic',
      # 'Drum and Bass',
      # 'Dubstep',
      # 'Folk & Acoustic',
      # 'Future Bass',
      # 'Future House',
      # 'Hip Hop',
      'House',
      # 'Ibiza', #! search
      'Indie',
      # 'Jazz',
      # 'Laid Back',
      # 'Pop',
      # 'R&B', #! 0. R&B Mix 37i9dQZF1EQoqCH7BwIYb7 # 1. R&B Mix 37i9dQZF1EIUJlbtxh7dav
      # 'Vapor Soul',
      # 'Vapor Twitch',
      '2020s',
      '2010s',
      '2000s',
      '90s',
      '80s',
   ]:
      playlist_name = i + ' Collection'
      playlist_id, sorted_track_uris = new_get_playlist_tracks(playlist_name)
      if playlist_id and sorted_track_uris:
         reorder_playlist(playlist_id, sorted_track_uris)
   else:
      print("Please provide a playlist name as an argument.")