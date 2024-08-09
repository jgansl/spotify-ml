# memoize for development repetitive 
# REFACTOR
# add genres updates artist
#! TODO update track and artists URI, genres, popularity, etc
#! test to check for artist track dups
#! playlist composure state machine and fine utning
#! group ovting and audio analysis; context for choice
#! all genre mix playlists - baised
# scan radios for artists
import json, os
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from spotipy.exceptions import SpotifyException

from time import sleep
from os import getenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from math import ceil
from datetime import datetime

from _constants import SCOPE

load_dotenv()
usr = getenv('usr')

auth = SpotifyOAuth(scope=SCOPE)#,open_browser=False, cache_path="./.cache.json")
sp   = Spotify(auth_manager=auth)

from enum import Enum

import pocketbase
from pocketbase import PocketBase
from pocketbase.client import ClientResponseError
pb = PocketBase('http://127.0.0.1:8092', 'en-US')

jprint = lambda x: print(json.dumps(x, indent=4))

tmp_dir_path = './db/tmp/'
filepath = lambda fp: f'{tmp_dir_path}/{fp}.json'
def save(obj, fp, i=2):
   if not os.path.exists(tmp_dir_path):
      os.makedirs(tmp_dir_path)
   with open(filepath(fp), 'w') as f:
      return json.dump(obj,f,indent=i)
   return

def load(fp):
   if os.path.exists(filepath(fp)):
      with open(filepath(fp), 'r') as f:
         return json.load(f)

# class Tags(Enum):
#    ARTIST = 1
#    PLAYLIST = 2
#    SAVED = 3
#    TRACK = 4

class Collections(Enum):
   PLAYLISTS = 1
   ARTISTS = 2
   SAVED = 3
   TRACKS = 4

class SAM():

   TEST = False #True

   playlists_db = []
   artists_db = pb.collection('artists').get_full_list()
   artists_map = {}
   tracks_db = pb.collection('tracks').get_full_list()
   tracks_map = {}
   playlists_sp = []

   def __init__(self):
      # get playlists, saved then manage alongside locally

      devices = sp.devices()['devices']
      self.device = [d for d in devices if d['is_active']]
      if len(self.device): 
         self.device = self.device[0]
      # jprint(self.device)
      # input('Continue?')
      
      #TODO - run everytime
      self._syncPlaylists()

      for a in self.artists_db:
         self.artists_map[a.spotify_id] = a
      
      for t in self.tracks_db:
         self.tracks_map[t.spotify_id] = t

      self.tracks_db = sorted(self.tracks_db, key=lambda d: d.release_date_str, reverse=True)
      #TODO filter for unheard
      tmp = [t for t in self.tracks_db if not t.heard]
      if self.device:
         print('Queuing tracks...')
         for t in tmp:
            if not t.uri[:50]:
               track = sp.track(t.spotify_id)
               t.uri = track['uri']
            pb.collection('tracks').update(
               t.id,
               {
                  'heard': True,
                  'uri' : t.uri
               }
            )

            sp.add_to_queue(t.uri, device_id=self.device['id'])
      # exit()

      #TODO meta
      self.scan_in_implicity_followed_playlists()

      
      
      return
   
   def _next(self, result): #pagination via API
      return sp.next(result)
   
   def _paginate(self, method_name, *args, **kwargs):
      data = getattr(sp, method_name)(*args, **kwargs)
      res = data['items']
      try:
         while data['next']:
            data = sp.next(data)
            res.extend(data['items'])
         return res
      except TypeError:
         # jprint(data)
         print(method_name, 'TypeError')
         jprint([*data])

   #TODO update if still following
   #TODO remove playlists if marked in PB
   # - dont use if not owned
   # - unfollow and remove from DB
   # update if owned
   def _syncPlaylists(self): 
      self.TEST = False
      print('Tracking playlists...')
      # get playlists, tracks and then manage locally - remove cache locally then apply move
      
      fp = 'playlists' + datetime.now().strftime("%Y%m%d%H%")
      self.playlists = load(fp) #TODO if TEST
      if not self.playlists or not self.TEST:
         self.playlists = self._paginate('current_user_playlists', limit=50)
         save(self.playlists, fp)
      # jprint(len(playlists))
      
      #TODO - two varaibles currently
      db_table = 'playlists'
      
      #bypass
      self.playlists_db = pb.collection(db_table).get_full_list()
      self.TEST = False
      return
      
      db_playlists = pb.collection(db_table).get_full_list()
      db_playlists_map = {}
      for p in db_playlists:
         db_playlists_map[p.spotify_id] = p
      db_playlists_map_keys = [*db_playlists_map]
      
      whitelist = [
         'Discover Weekly',
         'Release Radar',
         'Dance/Electronic Mix',
         'Folk & Acoustic Mix',
         'Hip Hop Mix',
         'House Mix',
         'Indie Mix',
         'Pop Mix',
         'R&B Mix',
         'Edmtrain: New Music Friday'
      ]
      for p in self.playlists_sp: #update if exists
         # pb.collection(Collections.PLAYLISTS).create(
         obj = {
            'spotify_id' : p['id'],
            'name' : p['name'],
            'description' : p['description'], #additive update
            'tags': [i[1:] for i in p['description'].split(" ") if len(i) and i[0] == '#'],
            'owner_id': p['owner']['id'],
            'uri': p['uri'],
            'implicity_follow': p['name'] not in whitelist and p['owner']['id'] == 'spotify',
         }
         # jprint(obj)
         if p['id'] in db_playlists_map_keys:
            pr = db_playlists_map[p['id']]
            if pr.owner_id != usr and pr.unfollow:
               pb.collection(db_table).delete( 
                  db_playlists_map[p['id']].id
               ) 
               sp.user_playlist_unfollow(usr, p['id'])
            else:
               pb.collection(db_table).update( 
                  db_playlists_map[p['id']].id, 
                  #TODO obj - keep database settings
                  {
                     'name' : p['name'],
                     'description' : p['description'], #additive update
                  } 
               )
               if pr.owner_id != usr and pr.implicitly_follow:
                  sp.user_playlist_unfollow(usr, p['id'])
         else: #sync updates back to spotify?
            pr = pb.collection(db_table).create( obj )
            if pr.owner_id == 'spotify' and pr.implicitly_follow:
               sp.user_playlist_unfollow(usr, p['id'])

      # owned and following
      # unowned - may be implicit

      #for unowned in db:
      p_ids = [p['id'] for p in playlists]
      self.playlists_db = pb.collection(db_table).get_full_list()
      for p in self.playlists_db:
         # guard
         if p.owner_id == usr: 
            continue

         if p.spotify_id not in p_ids and 'Radio' not in p.name:
            pb.collection(db_table).update( 
               p.id, 
               #TODO or unfollow
               {
                  "implicitly_follow": True
               } 
            )
         if 'Radio' in p.name:
            pb.collection(db_table).update( 
               p.id, 
               #TODO or unfollow
               {
                  "implicitly_follow": False
               } 
            )
            #TODO unfollow confirm
            # if p.spotify_id not in p_ids:
            #    pb.collection(db_table).delete( 
            #       db_playlists_map[p['id']].id
            #    ) 

         #if unowned not in playlists:
            #mark as implicitly followed
      
      if not self.TEST:
         self.playlists_sp = self._paginate('current_user_playlists', limit=50)

      return
      
   def insert_artist(self, data):
      if type(data) == str: #ID provided
         data = sp.artist(data)

      obj = {
         "spotify_id" : data['id'],
         'uri': data['uri'],
         "name": data['name'],
         "genres": [],
         # "popularity": data['popularity'], #TODO changes?; 0-100
         # "followers": data['followers']['total'], #TODO update
         # cross-tables
         # "queue": [],
         # "heard": []
      }
      if 'genres' in [*data]: #TODO update existing records
         obj['genres'] = data['genres']
      if 'popularity' in [*data]:
         obj['popularity'] = data['popularity']
      if 'followers' in [*data]:
         obj['followers'] = data['followers']

      record =  pb.collection('artists').create( obj )

      return record

   def insert_track(self, data):
      if type(data) == str: #ID provided
         data = sp.track(data)
         # print([*data])
         # input('Continue')
      else:
         data = data['track'] #! added_at
      
      try: 
         record = pb.collection('tracks').create(
            {
               "spotify_id" : data['id'],
               'uri': data['uri'],
               "name": data['name'],
               'heard': False,
               'liked': False,
               'cached': False,
               'playlists': [],
               'artists_name': ', '.join([a['name'] for a in data['artists']]),
               'artists': [a['id'] for a in data['artists']],
               'release_date_str': data['album']['release_date'],
            }
         )
      except pocketbase.utils.ClientResponseError:
         # TODO Already Exists...hmm not updating playlist?
         #TODO log
         print('insert_track...ClientResponseError', data['name'], data['uri'])
         # sleep(3)
         return
      return record
      
   #update artists?- popularity, genres, etc
   def scan_in_implicity_followed_playlists(self):
      print('\nscan_in_implicity_followed_playlists...')
      
      TEST = False
      count = 0

      lst1 = [p for p in self.playlists_db if p.owner_id != usr and p.implicitly_follow]
      if TEST:
         lst1 = lst1[:2]

      for p in lst1:
         print('\t'+p.name)

         # get tracks
         lst2 = self._paginate('playlist_items', p.spotify_id, limit=100) #TODO cache locally and retrieve
         if TEST:
            lst2 = lst2[:2]

         for t in lst2:
            try:
               if t['track']['id'] not in [*self.tracks_map]:
                  print('\t\t'+t['track']['name'])
                  trecord = self.insert_track(t)
                  if not trecord:
                     continue
               else:
                  trecord = self.tracks_map[t['track']['id']]
            except TypeError:
               print('\nscan_in_implicity_followed_playlists...Failure: retrieving track via ID')
               sleep(3)
               continue

            # update playlists
            trecord.playlists.append(p.name) #TODO name or id
            trecord.playlists.sort()
            res = pb.collection('tracks').update(
               trecord.id,
               {
                  'playlists': list(set(trecord.playlists))
               }
            )
            for a in t['track']['artists']:
               if a['id'] not in [*self.artists_map]: # make updates a single time elsewhere
                  # self.sync_artist(a)
                  self.insert_artist(a)
                  self.artists_db.append(a)
                  self.artists_map[a['id']] = a
         
         # # sync locally
         # self.tracks_db.append(res) #may produce two copies; refesh instead
         # self.tracks_map[t['track']['id']] = res
         # print(self.tracks_db)
         #TODO is dup
         self.tracks_db = pb.collection('tracks').get_full_list()
         for t in self.tracks_db:
            self.tracks_map[t.spotify_id] = t
         
         for i in range(10):
            print('TIMEOUT', i)
            sleep(1)
         count += 1
         print('Count', count)
      return


   def query_playlists():
      return
   
   def get_playlists(self):
      if not self.playlists:
         self.playlists = self.retrieve(PLAYLIST)

      return self.playlists
   
   def get_saved(self):
      return
   
   def track(self, track_id):
      # if not in pb, query and save to db
      # sp.
      return
   
   def tracks(self, track_id):
      return
   
   # storage of local that is linearly synced
   def move(self):
      # schedule

      return
   
   def trackPlaylists():
      for p in []:
         pass
      return

   def extract(self, data, key): #get_track_ids
      return [d[key] for d in data]
   
   def tmp():
      """
      for all genres - scan tracks to update genre - "mixes"
      for all daily mixes scan in unheard tracks
      """

      # for all unowned playlists, implicitly follow unless white listed, scan in tracks, artists, and link tracks to genre
      whitelist = [
         'Discover Weekly',
         'Release Radar',
      ]
      for i in self.get_unowned_playlists():

         # get playlist
         p = self.get_playlist(i) #if not implicity follow, check for playlist and implcity follow
         
         # get tracks from playlist
         tracks = self.get_tracks(p)
         
         # add track to db
         for t in tracks:
            self.insert_track(t) # implcity add artist
            # for a in self.extract(t['artists'], 'id') #hide artists
            #    self.insert_artist(a)
         
         # grab artist pb, spoyify
         
         # update artists
         
         pass

def new_releases():
   return

def categories():
   # ['href', 'items', 'limit', 'next', 'offset', 'previous', 'total']
   res = sp.categories()['categories']
   lst = []
   lst.extend(s.extract(res['items'], 'name'))
   while res['next']:
      res = sp.next(res)
      res = res['categories']
      lst.extend(s.extract(res['items'], 'name'))
      sleep(0.5)
   lst.sort()
   jprint(lst)

# DRY, test
# functional - 10 lines
# top down
# everything below should use SAM
# s.init()
# http://organizeyourmusic.playlistmachinery.com/#
# genres, #playlist, years, new
if __name__ == '__main__':
   load_dotenv()
   usr  = getenv('usr')
   auth = SpotifyOAuth( scope = SCOPE ) #,open_browser=False, cache_path="./.cache.json")
   sp   = Spotify( auth_manager = auth )
   s = SAM()

   # categories()

   # jprint([*sp.user_playlists('spotify')['items']])
   # jprint(s.extract(sp.user_playlists('spotify')['items'], 'name'))

   pass


# https://spotipy.readthedocs.io/en/2.22.1/
