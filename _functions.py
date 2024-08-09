from dotenv import load_dotenv
from os import environ, getenv

# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from spotipy.exceptions import SpotifyException

load_dotenv()
# usr = getenv('usr')

sp = None
user_id = None
def get_spotify_client():
   global sp, user_id

   # # Spotify API credentials
   # client_id = 'YOUR_CLIENT_ID'
   # client_secret = 'YOUR_CLIENT_SECRET'
   # redirect_uri = 'YOUR_REDIRECT_URI'
   # scope = 'user-library-read playlist-modify-public playlist-modify-private'

   # # Authenticate and create a Spotify API client
   # sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
   #                                                client_secret=client_secret,
   #                                                redirect_uri=redirect_uri,
   #                                                scope=scope))

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
get_spotify_client()


def log(message, stdout=False): #todo: reset
   if(stdout):
      print(str(message))
   with open('_debug.txt', 'a+') as f:
      f.write(str(message) + '\n')

###
#
# AI-Generated
#
###
def get_all_playlists():
   playlists = []
   results = sp.current_user_playlists()
   playlists.extend(results['items'])
   while results['next']:
      results = sp.next(results)
      playlists.extend(results['items'])
   return playlists

def get_playlist_tracks(playlist_id):
   tracks = []
   results = sp.playlist_tracks(playlist_id)
   tracks.extend(results['items'])
   while results['next']:
      results = sp.next(results)
      tracks.extend(results['items'])
   return [item['track']['id'] for item in tracks]

def get_liked_tracks():
   tracks = []
   results = sp.current_user_saved_tracks()
   tracks.extend(results['items'])
   while results['next']:
      results = sp.next(results)
      tracks.extend(results['items'])
   return [item['track']['id'] for item in tracks]

# todo: reversed
def move_tracks_to_playlist(track_ids, playlist_id):
   # Removing tracks in batches of 100
   for i in range(0, len(track_ids), 100):
      sp.playlist_add_items(playlist_id, track_ids[i:i+100])
      sp.current_user_saved_tracks_delete(track_ids[i:i+100])

def add_tracks_to_liked(track_ids):
   # Adding tracks in batches of 50 (Spotify API limit)
   for i in range(0, len(track_ids), 50):
      sp.current_user_saved_tracks_add(track_ids[i:i+50])

def remove_tracks_from_playlist(track_ids, playlist_id):
   # Removing tracks in batches of 100 (Spotify API limit)
   for i in range(0, len(track_ids), 100):
      sp.playlist_remove_all_occurrences_of_items(playlist_id, track_ids[i:i+100])
