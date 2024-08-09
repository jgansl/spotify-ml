import typing

# from json import *
# from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
from math import ceil
from os import getenv, system
# from time import sleep

from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from spotipy.exceptions import SpotifyException

import pocketbase
from pocketbase import PocketBase
from pocketbase.client import ClientResponseError

from _constants import *

load_dotenv()

auth = SpotifyOAuth( scope = SCOPE )#,open_browser=False, cache_path="./.cache.json")
sp   = Spotify( auth_manager = auth )

pb = PocketBase('http://127.0.0.1:8092', 'en-US')
usr = getenv('usr')
_playlists = None
_saved = None
#local sync
redis = {}

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


def scanInPlaylists():

   return


if __name__ == '__main__':

   # privateize playlists and sync to pb
   scanInPlaylists()

   pass