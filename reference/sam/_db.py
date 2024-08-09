
from _constants import ARTIST, PLAYLIST, SAVED, TRACK
from _functions import jprint, retrieve, sp, sleep
import pocketbase
from pocketbase import PocketBase
from pocketbase.client import ClientResponseError
pb = PocketBase('http://127.0.0.1:8092', 'en-US')
DEBUG = False
# test connection - print('Start in _functions')



def update_meta(key, value):
   #! if not exists
   if os.path.exists('_meta.json'):
      with open('_meta.json', 'r') as f:
         meta = json.load(f)
      meta[key] = value
      with open('_meta.json', 'w') as f:
         json.dump(data, f, indent=2)


_playlists = pb.collection('playlists').get_full_list()
_playlists_ids = [p.spotify_id for p in _playlists]
#! radios table
# for p in [p for p in _playlists if 'Radio' in p.name[-5:]]:
#    print(p.name)
#    pb.collection('playlists').delete(p.id)
def get_playlist(name, idx=None):
   global _playlists
   playlists = [p for p in _playlists if p.name == name]

   # more often to find one or more
   if len(playlists) == 1:
      return playlists[0]
   
   if len(playlists) > 1:  #! test
      if type(idx) == int:
         record = playlists[idx]
      else:
         # remove duplicates
         for idx, p in enumerate(playlists):
            print(str(idx)+'.', p.name, p.spotify_id)
         choice = ""
         while not choice.strip().isdigit():
            choice = input('Choice: ')
         choice = int(choice) #! assumes you're not stupid, but..
         record = playlists[choice]
   
   # if not pb
   else:
      search_results = [sr for sr in  sp_playlists if sr['name'] == name]
      if not search_results:
         # refresh playlists / find and add in pb
         search_results = [sr for sr in sp.search(q=name, limit=20, type="playlist")['playlists']['items'] if sr['name'] == name]
         # print([s['name'] for s in search_results])
         # input(len(search_results))
      
         # # search & insert if found
         # #! personal
         # results = retrieve(PLAYLIST, name=name)
         # if len(result) > 1:
         #    pass
         # result = results[0]

      if len(search_results) == 1:
         record = _insert_playlist(search_results[0])
      if len(search_results) > 1: #! dup
         for idx, sr in enumerate(search_results):
            print(str(idx)+'.', sr['name'], sr['id'])
         choice = ""
         while not choice.strip().isdigit():
            choice = input('Choice: ')
         choice = int(choice) #! assumes you're not stupid, but..
         record = _insert_playlist(search_results[choice])

      if len(search_results) == 0:
         input('Playlist not found: '+name) #! prevent program stop
   
   # return record
   return record

def _get_playlist_data(playlist, follow=True): # default value for insert
   data = {
      'description': playlist['description'],
      "follow": follow, # dont want to override existing values
      'name': playlist['name'],
      'owner': playlist['owner']['id'],
      'owner_name': playlist['owner']['display_name'],
      'sid': playlist['id'],
      'spotify_id': playlist['id'],
      # tags = [],
      'uri': playlist['uri'],
   }
   return data

def _insert_playlist(playlist):
   global _playlists
   data = _get_playlist_data(playlist)
   record = pb.collection('playlists').create(data)
   _playlists.append(record)
   if DEBUG:
      print('\tInserting Playlist:', playlist['name'])
   
   return record

def _update_playlist(playlist, record_id, follow, *args, **kwargs):
   record = pb.collection('playlists').update(
      record_id, 
      _get_playlist_data(playlist, follow)
   )
   return record


_artists = pb.collection('artists').get_full_list()
drr_artists = pb.collection('artists').get_full_list()
def get_artist(artist_id):
   global _artists
   artists = [a for a in _artists if a.spotify_id == artist_id]

   if len(artists) == 1:
      return artists[0]
   
   if len(artists) > 1: #! test
      for idx, a in enumerate(artists):
         print(str(idx)+'.', a.name, a.spotify_id)
      choice = ""
      while not choice.strip().isdigit():
         choice = input('Choice: ')
      choice = int(choice) #! assumes you're not stupid, but..
      record = artists[choice]
   
   else:
      artist = sp.artist(artist_id)
      sleep(0.1) #throttle -> queue?
      record = _insert_artist(artist)
      return

   return record

def _update_artist():
   print('TODO updateArtist')
   return

def _insert_artist(artist):
   global _artists
   data = {
      'follow': False,
      'genres': ','.join(artist['genres']), #search
      'genres_obj': artist['genres'], #currently not searchable via pb
      'heard': [],
      'name': artist['name'],
      'queue': [],
      'popularity': artist['popularity'],
      'sid': artist['id'],
      'spotify_id': artist['id'],
      'uri': artist['uri'],
   }

   record = pb.collection('artists').create(data)
   _artists.append(record)
   if DEBUG:
      print('\tInserting Artist:', artist['name'])
   
   return record


_tracks = pb.collection('tracks').get_full_list()
# help(pb.collection('tracks'))#! performance
def get_track(track_id, genre=None): #! check track as dict or string?
   global _tracks #! hashmap - external query rather than local
   # tracks = pb.collection('tracks').get_first_list_item("spotify_id == "+track_id )
   # get_list( 
   #    1, 30, {
   #       "spotify_id": track_id
   #       # "filter": "spotify_id" = "+track_id
   #    }
   #    # {
   #    #    "filter": "spotify_id = "+track_id 
   #    # }
   # ) #} && created > "2022-08-01 10:00:00"'})
   records = [t for t in _tracks if t.spotify_id == track_id]
   if len(records) == 1:
      #! update genre
      if genre: #! patch
         genre = genre.replace(" Mix", "") #! patch once
         genres = records[0].genres or []
         genres.append(genre)
         genres.sort()
         genres = list(set(genres))
         pb.collection('tracks').update(
            records[0].id, 
            {
               'genres': genres,
               'genres_str': ','.join(genres)
            }
         )
      return records[0]
   
   if len(records) > 1: #! test
      for idx, t in enumerate(records):
         print(str(idx)+'.', t.name, t.spotify_id)
      choice = ""
      while not choice.strip().isdigit():
         choice = input('Choice: ')
      choice = int(choice) #! assumes you're not stupid, but..
      record = records[choice]
   
   else:
      track = sp.track(track_id)
      sleep(0.1) #throttle -> queue?
      record = _insert_track(track, genre)
      return

   return record

#! ONLY FOR PATCH
def _get_track_data(t, genre=None):
   data = {
      'artists': [a['id'] for a in t['artists']],
      # 'artist': t['track']['artists'][0]['id'],
      # 'artist_genres': record.genres
      # 'cached': False,
      'genres': [],
      'liked': False,
      'name': t['name'],
      'new': True,
      'release_date': t['album']['release_date'], #! ['track']['album]?
      'sid': t['id'],
      # "specificity": 1,
      'spotify_id': t['id'],
      'uri': t['uri'],
   }
   if genre:
      data['genres']: [genre]

   return data
def _update_track(track, genre):
   print('TODO update_track')
   # artist
   return

#! Assumes DNE
def _insert_track(track, genre=None): #dup/wrapper of update_track
   global _tracks
   
   # try:
   #    t = track['track']
   # except KeyError:
   #    jprint(track)
   #    return
   t = track
   for artist in t['artists']:
      get_artist(artist['id']) #! contains all data needed?

   data = _get_track_data(t, genre)

   record = pb.collection('tracks').create(data)
   _tracks.append(record)
   if DEBUG:
      print('\tInserting Track:', t['name'])
   
   return record

_saved = None #private
def saved():
   global _saved
   if _saved:
      return _saved
   
   _saved = retrieve(SAVED)
   return _saved


#
#
# #! background
sp_playlists = retrieve(PLAYLIST)
for playlist in sp_playlists:
   if 'Radio' in playlist['name'][-5:]: #! radio mix
      if DEBUG:
         # print('Skipping Radio')
         pass
      continue
   #! if not follow , remove
   record = [p for p in _playlists if p.spotify_id == playlist['id']]
   #! more than one
   if len(record) > 1:
      input('More than one record for:'+playlist['name'])
   record = record[0] if record else None #!
   if record:
      record = _update_playlist(playlist, record.id, record.follow)
   else:
      record = _insert_playlist(playlist)
   
   if not record.follow: # implicity find with saerch if unfollow before recorded; records before removes
      print('Unfollowed:', record.name)
      sp.current_user_unfollow_playlist(record.spotify_id)
