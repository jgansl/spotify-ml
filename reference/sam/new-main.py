#! refactor; memorization for development
#! pi
#! check daily mix for recently released
#! remove old songs from recently released

from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from dotenv import load_dotenv
from json import dump, dumps, load
from math import ceil
from os import getenv, mkdir, path, system
from time import sleep
import typing

from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from spotipy.exceptions import SpotifyException

#from _constants import *

###
#  Constants
###
# types
ARTIST   = 'artist'
LIKED    = 'liked'
PLAYLIST = 'playlist'
TRACK    = 'track'

TAG_COLLECTION = '#collection'
TAG_MYMUSIC    = '#mymusic'

###
#  Utility Functions
###
jprint = lambda x: print(dumps(x, indent=4))

with open('_log.txt', 'w') as f:
   f.write(f'\n')
def log(msg: str, out=False):
   if out:
      print(msg)
   else:
      with open('_log.txt', 'a') as f:
         # f.write(f'{datetime.now()}: {msg}\n')
         f.write(f'{msg}\n\n')

def extract_ids(tracks):
   track_ids = []
   for track in tracks:
      try: 
         track_ids.append(track['track']['id'])
      except TypeError:
         log(f'\tError: a track does not have an id...')

   return track_ids

def init_spotify():
   # # Authenticate with Spotify API
   # client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
   # sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
   # return sp

   load_dotenv()
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

   return sp


liked = []
liked_tracks = []
liked_track_ids = []
def get_liked_tracks(update=False):
   global liked, liked_tracks, liked_track_ids
   log('Updating liked tracks...')

   if not update and liked:
      return liked
   else: 
      # Get user's liked tracks
      results = sp.current_user_saved_tracks()
      tracks = results['items']
      
      # Pagination to get all liked tracks
      while results['next']:
         results = sp.next(results)
         tracks.extend(results['items'])
      
      liked = tracks
      #todo: liked_tracks = [track['track'] for track in liked]
      liked_tracks = liked
      liked_track_ids = [track['track']['id'] for track in liked_tracks]
      
      return tracks


playlists = []
def get_playlists(update=False):
   global playlists
   log('Getting playlists...')

   if not update and playlists:
      return playlists
   else:
      # Get user's playlists
      results = sp.current_user_playlists()
      playlists = results['items']
      
      # Pagination to get all playlists
      while results['next']:
         results = sp.next(results)
         playlists.extend(results['items'])
      
      return playlists

def find_playlist(playlist_name: str, create=False, description=''): #! id?
   global playlists
   log(f'Searching for playlists: {playlist_name}...')
   results = []
   if len(playlists) == 0:
      #print('playlists not initialized')
      get_playlists()

   for playlist in playlists:
      if playlist['name'] == playlist_name:
         results.append(playlist)

   if len(results) == 1:
      log(f'\tFound 1 playlist for: {playlist_name}...')
      return results[0]
   elif len(results) > 1:
      log(f'\tFound Multiple playlists for: {playlist_name}...')
      #todo
   # # if len(results) < 1:
   elif create: # guarded by parameter - so any spotify playlists does not auto-create
      #! private does not work
      log(f'\tCreating playlist: {playlist_name}...')
      # Create playlist
      playlist = sp.user_playlist_create(sp.me()['id'], playlist_name, public=False, description=description)
      playlists.append(playlist)
      return playlist
   else:
      log(f'\tFound 0 playlists for: {playlist_name}...')
   return None


table_playlists_tracks = {}
def get_playlist_tracks(playlist_id, update=False):
   global table_playlists_tracks
   log(f'Getting playlist tracks for: {playlist_id}...') # todo:
   
   if not update and playlist_id in [*table_playlists_tracks]:
      log(f'Getting stored playlist tracks for: {playlist_id}...') # todo:
      return table_playlists_tracks[playlist_id]
   else:
      log(f'Requesting playlist tracks for: {playlist_id}...') # todo:
      # Get playlist tracks
      results = sp.playlist_tracks(playlist_id)
      tracks = results['items']
      
      # Pagination to get all tracks
      while results['next']:
         results = sp.next(results)
         tracks.extend(results['items'])
      
      # # Get track details
      # for item in tracks:
      #    track = item['track']
      #    track_id = track['id']
      #    track_name = track['name']
      #    artist = track['artists'][0]['name']
      #    album = track['album']['name']
      #    release_date = track['album']['release_date']
      #    popularity = track['popularity']
         
      #    # Process track details
      #    print(f"Track ID: {track_id}")
      #    print(f"Track Name: {track_name}")
      #    print(f"Artist: {artist}")
      #    print(f"Album: {album}")
      #    print(f"Release Date: {release_date}")
      #    print(f"Popularity: {popularity}")
      #    print("\n")

      table_playlists_tracks[playlist_id] = tracks

      return tracks

def get_recent_tracks(playlist_id):
   # # Get playlist tracks
   # results = sp.playlist_tracks(playlist_id)
   # tracks = results['items']
   
   # # Pagination to get all tracks
   # while results['next']:
   #    results = sp.next(results)
   #    tracks.extend(results['items'])

   log(f'Getting recent tracks for: {playlist_id}...') # todo:

   tracks = get_playlist_tracks(playlist_id)
   
   # Current date and date 365 days ago
   current_date = datetime.now()
   one_year_ago = current_date - timedelta(days=90)
   
   # Filter tracks less than 365 days old
   recent_tracks = []
   for item in tracks:
      track = item#['track'] #!todo: extract_ids update
      album_release_date = track['track']['album']['release_date']
      
      # Handle different date formats
      if len(album_release_date) == 4:
         album_release_date = datetime.strptime(album_release_date, "%Y")
      elif len(album_release_date) == 7:
         album_release_date = datetime.strptime(album_release_date, "%Y-%m")
      else:
         album_release_date = datetime.strptime(album_release_date, "%Y-%m-%d")
      
      if album_release_date > one_year_ago:
         recent_tracks.append(track)
   
   return recent_tracks

def transfer_tracks(source_id: str, destination_id: str, track_ids: list):
   # if src is dict, extract id
   source_id = source_id['id'] if isinstance(source_id, dict) else source_id
   # if dest is dict, extract id
   destination_id = destination_id['id'] if isinstance(destination_id, dict) else destination_id

   #todo: check if str is name and not ID; pytests; dry run

   if source_id == LIKED:
      log(f'Removing {len(track_ids)} tracks from liked...')
      # batch remove from liked
      for i in range(ceil(len(track_ids)/50)): #todo: 1by1
         sp.current_user_saved_tracks_delete(track_ids[i*50:(i+1)*50])
   elif source_id != None:
      log(f'Removing {len(track_ids)} tracks from: {source_id}...')
      # batch remove from source
      for i in range(ceil(len(track_ids)/100)):
         sp.playlist_remove_all_occurrences_of_items(source_id, track_ids)
   


   if destination_id == LIKED:
      log(f'Adding {len(track_ids)} tracks to liked...')
      # batch add to liked
      for i in range(ceil(len(track_ids)/50)):
         sp.current_user_saved_tracks_add(track_ids[i*50:(i+1)*50])
   elif destination_id != None:
      log(f'Adding {len(track_ids)} tracks to: {destination_id}...')
      # batch add to destination
      for i in range(ceil(len(track_ids)/100)):
         sp.playlist_add_items(destination_id, track_ids[i*100:(i+1)*100])

   return

def search_for_playlist(playlist_name, owner_id='spotify'):
   log(f'Searching Spotify for playlist: {playlist_name}...')

   key = 'playlist'
   results = sp.search(q=playlist_name, type='playlist', limit=50)

   # jprint(results['playlists']['total'])
   # input()
   
   # filter results for playlists with the exact name by the user or by spotify
   playlists = []
   for playlist in results['playlists']['items']:
      if (
         playlist['name'] == playlist_name and
         playlist['owner']['id'] == owner_id
      ):
         playlists.append(playlist)
   
   if len(playlists) == 1:
      log(f'\tFound 1 playlist for: {playlist_name}...')
      return playlists[0]
   elif len(playlists) > 1:
      log(f'\tFound Multiple playlists for: {playlist_name}...')
      #todo
   # # if len(playlists) < 1:
   else:
      log(f'\tFound 0 playlists for: {playlist_name}...')
   return None

def update_new_with_discover_weekly(): #! only once a week
   # if today is not monday, return:
   if datetime.now().weekday() != 0:
      return

   # find playlist name 'New' by sp.me()
   p_new = find_playlist('New')


   # get all playlists named 'Discover Weekly' or 'Release Radar'
   plst_discover_weekly = [p for p in playlists if 'Discover Weekly' in p['name']]

   # for each playlist, get the tracks
   for p in plst_discover_weekly:
      tracks = get_playlist_tracks(p['id'])
      track_ids = extract_ids(tracks)
      transfer_tracks(None, p_new['id'], track_ids)

def update_new_with_release_radar(): #! only once a week
   # if today is not friday, return:
   if datetime.now().weekday() != 4:
      return

   # find playlist name 'New' by sp.me()
   p_new = find_playlist('New')


   # get all playlists named 'Discover Weekly' or 'Release Radar'
   plst_release_radar   = [p for p in playlists if 'Release Radar' in p['name']]

   # for each playlist, get the tracks
   for p in plst_release_radar:
      tracks = get_playlist_tracks(p['id'])
      track_ids = extract_ids(tracks)
      transfer_tracks(None, p_new['id'], track_ids)


def partition_new():
   """
   machine learning technique to divide tracks in "New" playlist into new playlist by most appropriate genre
   """
   p_new = find_playlist('New')
   tracks = get_playlist_tracks(p_new['id'])

   # # get audio features for each track
   # audio_features = []
   # for i in range(ceil(len(tracks)/100)):
   #    audio_features.extend(sp.audio_features([track['track']['id'] for track in tracks[i*100:(i+1)*100]]))
      
   # # get the most appropriate genre for each track
   # genres = []
   # for i in range(ceil(len(audio_features)/100)):
   #    genres.extend(sp.recommendation_genre_seeds())

   # # create a new playlist for each genre
   # for genre in genres:

   #! remove from 'New' if track in collection

def cycle_tracks():
   global liked_tracks #, playlists

   log('Cycling Tracks...\n')

   # Get "Cycle" playlist ID
   # playlists = sp.current_user_playlists()
   # cycle_playlist_id = None
   # for playlist in playlists['items']:
   #    if playlist['name'].lower() == 'cycle':
   #       cycle_playlist_id = playlist['id']
   #       break
   cycle_playlist_id = find_playlist('Cycle')['id']

   #! memories - dont add to collection..? double, implicit - 365

   if cycle_playlist_id is None:
      print("Cycle playlist not found")
      return

   # # Get tracks from "Cycle" playlist
   # results = sp.playlist_tracks(cycle_playlist_id)
   # cycle_tracks = results['items']
   
   # # Pagination to get all tracks
   # while results['next']:
   #    results = sp.next(results)
   #    cycle_tracks.extend(results['items'])
   cycle_tracks = get_playlist_tracks(cycle_playlist_id)
   
   # Calculate 10% of the tracks to add to liked songs
   ten_percent_count = max(1, len(cycle_tracks) // 10)
   tracks_to_add = [track['track']['id'] for track in cycle_tracks[:ten_percent_count]]
   
   # # Get current liked songs
   # results = sp.current_user_saved_tracks()
   # liked_tracks = results['items']
   
   # # Pagination to get all liked tracks
   # while results['next']:
   #    results = sp.next(results)
   #    liked_tracks.extend(results['items'])
   
   # Current date and date 3 days ago
   three_days_ago = datetime.now() - timedelta(days=3)
   
   # Remove tracks older than 3 days from liked songs and add to "Cycle" playlist
   tracks_to_remove = []
   tracks_to_move_to_cycle = []
   for item in liked_tracks:
      track_id = item['track']['id']
      added_at = datetime.strptime(item['added_at'], "%Y-%m-%dT%H:%M:%SZ")
      
      if added_at < three_days_ago:
         tracks_to_remove.append(track_id)
         if track_id not in tracks_to_add:
            tracks_to_move_to_cycle.append(track_id)
   
   if tracks_to_move_to_cycle:
      # sp.user_playlist_add_tracks(sp.current_user()['id'], cycle_playlist_id, tracks_to_move_to_cycle)
      transfer_tracks(None, cycle_playlist_id, tracks_to_move_to_cycle)
   
   # Add 10% of tracks from "Cycle" playlist to liked songs
   if tracks_to_add: #todo: batch
      # sp.current_user_saved_tracks_add(tracks_to_add)   
      transfer_tracks(cycle_playlist_id, LIKED, tracks_to_add)
   
   if tracks_to_remove:
      # sp.current_user_saved_tracks_delete(tracks_to_remove)
      transfer_tracks(LIKED, None, tracks_to_remove)
   
   

if __name__ == '__main__':
   # todo: benhchmark and optimize
   sp = init_spotify()

   get_playlists() # update globals
   # plst_collections = [p for p in playlists if ' Collection' in p['name'][-11:]]
   # for p in plst_collections:
   #    log(p['name'])
   # p_cycle = find_playlist('Cycle')
   # p_cache = find_playlist('Cache')
   # # iteratively fetch tracks in background globals['p_cycle'] = p_cycle
   
   get_liked_tracks() # update globals
   
   # #todo: async - update days playlist

   # plst_mymusic = [p for p in sp.current_user_playlists()['items'] if TAG_MYMUSIC in p['description']]
   # for p in plst_mymusic:
   #    log(p['name'])

   # run only once a day, checking and update data/meta.json
   meta_filename = 'data/meta.json'
   meta = {'last_updated': ''}
   # check that data folder exists and make if not
   if not path.exists('data'):
      mkdir('data')
   if not path.exists(meta_filename):
      with open(meta_filename, 'w') as f:
         dump(meta, f)
   with open(meta_filename, 'r') as f:
      meta = load(f)


   recently_released = find_playlist(f'Recently Released', create=True, description='')
   log('Recently Released:')

   # remove tracks that were released more than 365 days ago from recently released
   recently_released_tracks = get_playlist_tracks(recently_released['id'])
   for track in recently_released_tracks:
      album_release_date = track['track']['album']['release_date']
      if len(album_release_date) == 4:
         album_release_date = datetime.strptime(album_release_date, "%Y")
      elif len(album_release_date) == 7:
         album_release_date = datetime.strptime(album_release_date, "%Y-%m")
      else:
         album_release_date = datetime.strptime(album_release_date, "%Y-%m-%d")
      if album_release_date < datetime.now() - timedelta(days=365):
         #! transfer_tracks(None, recently_released['id'], [track['track']['id']])
         transfer_tracks(recently_released['id'], None, [track['track']['id']])


   today = datetime.now().date().strftime("%Y-%m-%d")


   hidden = find_playlist('Hidden', create=True, description='')
   hidden_tracks = get_playlist_tracks(hidden['id'])
   hidden_tracks_ids = extract_ids(hidden_tracks)

   #! prevent adding if removed
   if meta.get('last_updated', None) != today:
      for genre in [ #! scan in genres.json
         #! followed only  ?
         'Beach',
         'Chill',
         'Dance/Electronic',
         'Drum and Bass',
         'Dubstep',
         'Folk & Acoustic',
         'Future Bass',
         'Future House',
         'Hip Hop',
         'House',
         'Ibiza', #! search
         'Indie',
         #'Jazz',
         'Jungle',
         'Laid Back',
         'Pop',
         'R&B', #! 0. R&B Mix 37i9dQZF1EQoqCH7BwIYb7 # 1. R&B Mix 37i9dQZF1EIUJlbtxh7dav
         'Rizz',
         'Rock',
         # 'Vapor Soul',
         'Vapor Twitch',
         #! only if in cache
         # '2020s',
         # '2010s', #! to move out of 2010s
         # '2000s',
         # '90s',
         # '80s',
      ]:
         if meta.get(f'mix_collection {genre}', None) == today:
            continue

         mix = search_for_playlist(f'{genre} Mix') #! memoization; add to playlist local map?
         collection = find_playlist(f'{genre} Collection', create=True, description=f'{TAG_COLLECTION}')
      

         if not mix:
            log(f'\tError: {genre} Mix not found...')
            continue
         if not collection:
            log(f'\tError: {genre} Collection not found...')
            continue

         mix_tracks = get_recent_tracks(mix['id'])
         mix_tracks_ids = extract_ids(mix_tracks)
         collection_tracks = get_playlist_tracks(collection['id'])
         collection_tracks_ids = extract_ids(collection_tracks)
         rr_tracks = get_playlist_tracks(recently_released['id'])
         rr_tracks_ids = extract_ids(rr_tracks)

         # get the tracks that mix_tracks has the collection_tracks does not
         new_tracks_ids = [track_id for track_id in mix_tracks_ids if track_id not in rr_tracks_ids]
         print(f'{genre}: {len(new_tracks_ids)} new tracks added')
         
         transfer_tracks(None, recently_released['id'], new_tracks_ids)  #! prevent from adding multiple times; hidden -> pb mark? keep in hidden until older than 365 days?
         # transfer_tracks(None, collection['id'], new_tracks_ids)  #! prevent from adding multiple times; hidden -> pb mark? keep in hidden until older than 365 days?
         # add to newly released and prevent readding
         # transfer_tracks(None, LIKED, new_tracks_ids)
         #! todo remove tracks older than 90 days

         # update data
         meta['mix_collection ' + genre] = today
         with open('data/meta.json', 'w') as f:
            dump(meta, f, indent=2)
      


      # todo: meta
      update_new_with_discover_weekly()

      # todo: meta
      # cycle_tracks() #! additive for the day

      # save updated metadata
      meta['last_updated'] = today
      with open('data/meta.json', 'w') as f:
         dump(meta, f, indent=2)

      rr_tracks = get_playlist_tracks(recently_released['id'])
      rr_tracks_ids = extract_ids(rr_tracks)
      #! release radar
      for num in [1,2,3,4,5,6]:
         mix = search_for_playlist(f'Daily Mix {num}') #!
         print(mix['uri'])
         mix_tracks = get_recent_tracks(mix['id'])
         mix_tracks_ids = extract_ids(mix_tracks)
         new_tracks_ids = [track_id for track_id in mix_tracks_ids if track_id not in rr_tracks_ids and track_id not in hidden_tracks_ids]
         transfer_tracks(None, recently_released['id'], new_tracks_ids)

   rr_tracks = get_playlist_tracks(recently_released['id'])
   # find tracks released more than 90 days ago
   for t in rr_tracks:
      album_release_date = t['track']['album']['release_date']
      if len(album_release_date) == 4:
         album_release_date = datetime.strptime(album_release_date, "%Y")
      elif len(album_release_date) == 7:
         album_release_date = datetime.strptime(album_release_date, "%Y-%m")
      else:
         album_release_date = datetime.strptime(album_release_date, "%Y-%m-%d")
      if album_release_date < datetime.now() - timedelta(days=90):
         try:
            sp.add_to_queue(t['track']['id'])
         except: 
            exit()
         transfer_tracks(recently_released['id'], None, [t['track']['id']])
         transfer_tracks(hidden['id'], None, [t['track']['id']])

      #! move older than 365 from cycle/liked if in collection

   percent1 = [p for p in playlists if '#percent-1' in p['description']][0]

   tmp2 = datetime.now().timetuple().tm_yday
   tmp3 = round(tmp2 * 100 / 366, 2)
   rem = 366 - tmp2
   sp.playlist_change_details(percent1['id'], name=str(rem)+' Days Left - '+str(tmp3)+'% of 2024')

   #! 5/6 years
   # #get number of days left in year 2024
   # remaining_days = 366 - datetime.now().timetuple().tm_yday
   tmp = [p for p in playlists if '#percent-2' in p['description']][0]
   day_count = datetime.now() - datetime(2024, 2, 26)
   rem = 365*6 + 2
   rem = round(day_count.days * 100 / rem, 2)
   sp.playlist_change_details(tmp['id'], name=str(day_count.days)+' Days - '+str(rem)+'% of 6 Years')

   # get number of days since Feburary 26, 1995
   # 3951/26298 - 15.03% - 60 years
   day_count = datetime.now() - datetime(1995, 2, 26)
   numdays = day_count.days
   tmp = [p for p in playlists if '#percent-3' in p['description']][0]
   percent = round(numdays * 100 / 26298, 2)
   sp.playlist_change_details(tmp['id'], name=str(percent)+'% of 72 Years')
