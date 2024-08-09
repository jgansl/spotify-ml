"""
functional programming & tests

# reserved:
- p
"""
from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from dotenv import load_dotenv
from json import dump, dumps, load
from math import ceil
from os import getenv, system
from time import sleep
import typing

from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from spotipy.exceptions import SpotifyException

from _constants import *
# from _db import sp_playlists

jprint = lambda x: print(dumps(x, indent=4))

# import pocketbase
# from pocketbase import PocketBase
# from pocketbase.client import ClientResponseError
# pb = PocketBase('http://127.0.0.1:8092', 'en-US')
# print('Start in _functions')
# try:
#    # print('PB not running but uhh...', pb)
#    print('PB running:', pb)
#    system('clear')
# except:# pocketbase.utils.ClientResponseError:
#    print('PB not running')
#    exit()

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


def _paginate(func, *args, **kwargs):
   
   data = []
   lim = 50  # ! if not lim
   pack = {}
   if "lim" in kwargs.keys():
      lim = kwargs["lim"]
   pack["limit"] = lim
   if "pid" in kwargs.keys():
      pack['user'] = usr
      pack['playlist_id'] = kwargs["pid"]

   # init
   res = func(**pack)
   total = res["total"]
   data = res['items']

   if total > lim:
      with ThreadPoolExecutor(max_workers=15) as executor:
            future_res = {
               executor.submit(func, offset=i*lim, **pack): i for i in range(1, ceil(total / lim))
            }
            for future in as_completed(future_res):
               data.extend(future.result()["items"])

      # sort
   return data

def retrieve(typ, pid=None, *args, **kwargs,):  # !TIDS
   # global sp, cache  # !cache
   mp = {
      PLAYLIST: sp.current_user_playlists,
      SAVED: sp.current_user_saved_tracks,
      TRACK: sp.user_playlist_tracks,
   }

   if typ.lower().strip() == SAVED:
      # if 'saved' not in [*mem]:
      #     mem['saved'] = {"name": "saved", "tracks": None, "tids": None}
      # if mem['saved']['tracks']:
      #     return mem['saved']['tracks']
      # else:
      res = _paginate(sp.current_user_saved_tracks, *args, **kwargs)
      for t in res:
         try:
            del t['track']['album']['available_markets']
         except TypeError:
            pass
         try:
            del t['track']['available_markets']
         except TypeError:
            pass
      return res
   elif typ.lower().strip() == PLAYLIST:
      res = _paginate(sp.current_user_playlists, *args, **kwargs)
      # id & type ++> pid and sid same?
      #! ? name, history, keywords..

      return res
   elif typ.lower().strip() == TRACK:
      res = _paginate(sp.user_playlist_tracks, pid=pid,
                        *args, user=usr, **kwargs)
      for t in res:
         try:
            del t['track']['album']['available_markets']
            del t['track']['available_markets']
         except: pass
      return res
   # elif typ.lower().strip() == ARTIST_ALBUMS:  # multiple artiusts?
   #    pass

def move(src, dst, items=[], owned=True, limit=50):
   def parallel(src, dst, items=[], owned=True):
      # print(dst)
      if dst:
         if dst.lower() == SAVED:
            try:
               snpsht = sp.current_user_saved_tracks_add(tracks=items)
            except SpotifyException:
               for i in items:
                  try:
                     snpsht = sp.current_user_saved_tracks_add(tracks=[i])
                  except: #!
                     pass
         else:
            try:
               snpsht = sp.user_playlist_add_tracks(
                  user=usr, playlist_id=dst, tracks=items
               )
               if snpsht:
                  pass  # log(0, snpsht)  # log(0, err)
            # non existent IDs - spotipy.client.SpotifyException, requests.exceptions.HTTPError
            except SpotifyException:
               grace = False
               for i in items:
                  try:
                     snpsht = sp.user_playlist_add_tracks(
                        user=usr, playlist_id=dst, tracks=[i]
                     )
                     if snpsht:
                        pass  # print("ADDING", snpsht)
                  except SpotifyException:
                     if not grace:
                        #!log(1, "Skipped adding track..")
                        pass
                     grace = True
                     continue

      # src removal
      if src:
         if src.lower() == SAVED:
            snpsht = sp.current_user_saved_tracks_delete(tracks=items)
         elif src:
            if owned:
               # TODO internally check that it is a list of string ids
               snpsht = sp.user_playlist_remove_all_occurrences_of_tracks(
                  user=usr, playlist_id=src, tracks=items, snapshot_id=None
               )
               # sp.user_playlist_remove_tracks(user=usr, playlist_id=lst[i]['pid'], tracks=t)
               # if snpsht:
               #    print("REMOVE", snpsht)
      return
   #! AttributeError: 'dict' object has no attribute 'lower' -> ID, check if dict
   if type(src) == 'dict':
      src = src['id']
   if type(dst) == 'dict':
      dst = dst['id']
   if src and SAVED in src.lower(): # Id not passed if error
      src = SAVED
   if dst and SAVED in dst.lower(): # Id not passed if error
      dst = SAVED
   # jprint(items)
   if not len(items):
      return

   executor = ThreadPoolExecutor(max_workers=7)
   reqs = len(items) // limit
   # print(reqs)

   for i in range(reqs):
      print("\tSubmitted", str(i))
      # executor.submit(parallel, src, dst,
      #                   items[i * 50: i * 50 + 50], owned=owned)
      parallel(src, dst, items[i * 50: i * 50 + 50], owned=owned)
   # executor.submit(parallel, src, dst,
   #                items[reqs * 50: len(items)], owned=owned)
   parallel(src, dst, items[reqs * 50: len(items)], owned=owned)
   # try:
   if src == SAVED or dst == SAVED:
      saved = retrieve(SAVED) # lazy init
      sids = [s['track']['id'] for s in saved]
   # print('SAVED', len(sids))
      # saved = sp.retrieve(SAVED)
      # sids = [s['track']['id'] for s in saved]
   # except:
   #    print('sids not updated')
   return 

def get_ids(tracks): #!
   # if type(tracks[0] == playlist):
   # if type(tracks[0] == record):
   # else:
   
   #[t['track']['id'] for t in tracks]
   lst = []
   for t in tracks:
      try:
         lst.append(t['track']['id'])
      except (KeyError, TypeError):
         continue

   return lst

_sp_playlists = retrieve(PLAYLIST)
def pname(name): #! more than 1
   print('pname- looking for:', name)
   global _sp_playlists #! dup of _db
   res = [p for p in _sp_playlists if p['name'] == name]
   if len(res) == 0:
      # create playlist
      res = [sp.user_playlist_create(usr, name, public=False, description='#collection')]
   elif len(res) > 1:
      for p in res:
         print(p['name'], p['id'])
      input(name+': more than on result')
   
   return res[0]

# playlist_map = {}
# _playlists = None #private
# def playlists(): #TODO cache - development; #TODO return records - getPlaylist
#    global _playlists
#    if _playlists:
#       return _playlists
   
#    _playlists = retrieve(PLAYLIST)
#    return _playlists

# _saved = None #private
# def saved():
#    global _saved
#    if _saved:
#       return _saved
   
#    _saved = retrieve(SAVED)
#    return _saved

# ###
# #
# # DB
# #
# ###
# def updatePlaylist(record_id, data):
#    return pb.collection('playlists').update(record_id, data)
# def insertPlaylist(p):
#    #! if type(data) == str: #ID provided
#    #    data = retrieve(PLAYLIST)
#    # else:
#    #    data = data['track'] #! added_at

#    # try: 
#    pb.collection('playlists').create(
#       {
#          "sid": p['id'],
#          "spotify_id": p['id'],
#          "name": p['name'],
#          "description": p['description'],
#          'owner': p['owner']['id'],
#          'owner_name': p['owner']['display_name'],
#          "follow": True,
#          "uri": p['uri'],
#       }
#    )
#    return



# # db_heard = pb.collection('heard').get_full_list()
# # db_heard_ids = [t.spotify_id for t in db_heard]

# # db_queue = pb.collection('queue').get_full_list()
# # # print(len(db_queue)) #! had to restart; meaning updlicates and errors - unique though
# # db_queue_ids = [t.spotify_id for t in db_queue]
# # # for i in db_queue:
# # #    pb.collection('queue').delete(i.id)
# # # db_queue = pb.collection('queue').get_full_list()
# # # db_queue_ids = [t.spotify_id for t in db_queue]

# db_tracks = pb.collection('tracks').get_full_list()
# db_track_ids = [t.spotify_id for t in db_tracks]
# def insertTrack(data, table='tracks', genre=None):
#    if type(data) == str: #ID provided
#       data = sp.track(data)
#    #    if data:
#    # else:
#    data = data['track'] #! added_at

#    #! if t['id'] not in 
#    if not data or data['id'] in db_track_ids:
#       # print('\tExists')
#       return
   
#    try: 
#       print('\tNew')
#       record = pb.collection(table).create(
#          { # TODO
#             "sid" : data['id'],
#             "spotify_id" : data['id'],
#             "name": data['name'],
#             'new': True,
#             # 'liked': False,
#             # 'cached': False,
#             # 'playlists': [],
#             # 'artists_name': ', '.join([a['name'] for a in data['artists']]),
#             # 'artists': [a['id'] for a in data['artists']],
#             'release_date': data['album']['release_date'],
#             'uri': data['uri'],
#          }
#       )
#       db_track_ids.append(data['id'])
#       return record
#    except pocketbase.utils.ClientResponseError:
#       # TODO Already Exists...hmm not updating playlist?
#       #TODO log
#       print('insert_track...ClientResponseError', data['name'], data['uri'])
#       # sleep(3)
#       return

   
   

# db_playlist_map = {}
# db_playlists = pb.collection('playlists').get_full_list()
# for p in db_playlists:
#    db_playlist_map[p.spotify_id] = p
# db_playlist_ids = [p.spotify_id for p in db_playlists]
# def syncPlaylistsToDB():
#    global db_playlist_ids

#    for p in playlists():
#       # if p['id'] not in db_playlist_ids:
#       # print('sync playlist to DB:', p['name'])
#       try:
#          updatePlaylist(
#             db_playlist_map[p['id']].id, 
#             {
#                'owner_name': p['owner']['display_name'],
#             }
#          )
#       except KeyError:
#          record = insertPlaylist(p)
#    return
# def syncDBToPlaylists():
#    #update description
#    #update public
#    #update public
#    return


# db_artist_map = {}
# db_artists = pb.collection('artists').get_full_list()
# for p in db_artists:
#    db_artist_map[p.spotify_id] = p
# db_artist_ids = [p.spotify_id for p in db_artists]
# def addHeardToArtists(t):
#    artist_id = t['track']['artists'][0]['id']
#    if artist_id not in [*db_artist_map]:
#       a = getArtist(artist_id)

#    a = db_artist_map[artist_id]
#    tracks = a.heard
#    tracks.append(t['track']['id'])
#    pb.collection('artists').update(
#       a.id,
#       {
#          'heard': list(set(tracks))
#       }
#    )
#    return
# def addQueueToArtists(t):
#    artist_id = t['track']['artists'][0]['id']
#    if artist_id not in [*db_artist_map]:
#       a = getArtist(artist_id)
   
#    a = db_artist_map[artist_id]
#    tracks = a.queue
#    tracks.append(t['track']['id'])
#    pb.collection('artists').update(
#       a.id,
#       {
#          'queue': list(set(tracks).difference(set(a.heard)))
#       }
#    )
#    return
# def insertArtist(data): #assumes dict
#    global db_artists, db_artist_ids, db_artist_map
#    if type(data) == 'str': #ID provided
#       data = sp.artist(data)
#       sleep(0.5)
#    try: 
#       record = pb.collection('artists').create(
#          {
#             "sid" : data['id'],
#             "spotify_id" : data['id'],
#             "name": data['name'],
#             "genres": ", ".join(data['genres']),
#             "genres_obj": data['genres'],
#             'queue': [],
#             'heard': [],
#             "popularity": data['popularity'], #TODO changes?; 0-100
#             "followers": data['followers']['total'], #TODO update
#             # 'liked': False,
#             # 'cached': False,
#             # 'playlists': [],
#             # 'artists_name': ', '.join([a['name'] for a in data['artists']]),
#             # 'artists': [a['id'] for a in data['artists']],
#             # 'release_date': data['album']['release_date'],
#             'uri': data['uri'],
#          }
#       )
#       db_artists.append(record)
#       db_artist_ids.append(record.spotify_id)
#       db_artist_map[record.spotify_id] = record
#       return record
#    except pocketbase.utils.ClientResponseError:
#       print(a['name'], 'ERROR Creating')


# def getArtist(artist_id: str):
#    db_results = [p for p in db_artists if p.spotify_id == artist_id]

#    if len(db_results):
#       return db_results[0]
#    else:
#       a = sp.artist(artist_id)
#       record = insertArtist(a)
#       sleep(0.5)
#       return record

# def getPlaylist(name: str):

#    #! flip, insert and return record
   
#    # print('Checking playlist DB for: ' + name + '\n')
#    db_results = [p for p in db_playlists if p.name == name]
#    if len(db_results) > 1:
#       for entry in db_results:
#          print(entry.name)
#       print()
#       print('More that 1 result for: ' + name)
      
#       choice = input('Choose one: ')
#       while not choice.isdigit():
#          choice = input('Choose one: ')
#       choice = int(choice)
#    else:
#       choice = 0
   

#    if len(db_results):
#       return db_results[choice]
#    else: # search following
#       res = []
#       # print(len(playlists()))
#       for p in playlists():
#          if p['name'] == name:
#             if p['id'] not in db_playlist_ids:
#                record = insertPlaylist(p) #! update local
#                db_playlists.append(p)
#                db_playlist_ids.append(p['id'])
#                db_playlist_map[p['id']] = record
#                res.append(record)
#             else:
#                res.append(db_playlist_map[p['id']])
      
#       if len(res) > 1:
#          for entry in res:
#             print(entry['name'])
#          print()
#          print('More that 1 result for: ' + name)
         
#          choice = input('Choose one: ')
#          while not choice.isdigit():
#             choice = input('Choose one: ')
#       else:
#          choice = 0

#       if len(res):
#          return res[choice]


# def getTracks(pid:str):
#    if False:
#       pass #!
#    else:
#       return retrieve(TRACK, pid=pid)