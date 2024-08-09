# import json
from ___sam import *
# import re
import os
from spotipy.exceptions import SpotifyException
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
#import ytm
# from ytm import YouTubeMusic
from ytmusicapi import YTMusic # https://ytmusicapi.readthedocs.io/en/latest/setup.html

jprint = lambda x: print(json.dumps(x,indent=2))

mem = SAM(sp)
e   = ThreadPoolExecutor(max_workers=5)
# api = YouTubeMusic()
# jprint(list(api._methods))
# results = api.search('alt-j')
# jprint(list(results))


ytmusic = YTMusic('headers_auth.json')
# playlistId = ytmusic.create_playlist('test', 'test description')

def searchForYTrack():
   # YTMusic.search(query: str, filter: str = None, scope: str = None, limit: int = 20, ignore_spelling: bool = False) → List[Dict[KT, VT]]
   res = ytmusic.search('Oasis Wonderwall')
   return res
## search_results = searchForYTrack()
#jprint(search_results)
## ytmusic.add_playlist_items(playlistId, [search_results[0]['videoId']])

#
#
#
# YTMusic.get_library_songs(limit: int = 25, validate_responses: bool = False, order: str = None) → List[Dict[KT, VT]]
ysaved = ytmusic.get_library_songs(500)
# print(len(ysaved))
# jprint([i['title'] for i in ysaved])
# jprint(ysaved[0])

ypid = mem.pname('ytm')
ytks = mem.get_track_ids(mem.pname('ytm'))
#sync spo with yt
for ytrack in ysaved:
   os.system('clear')
   idx = ''
   # sp.search(q, limit=10, offset=0, type='track', market=None)
   tit = ytrack['title'].lower()
   if tit in [ #testing
      'trouble (feat. chronixx & maverick sabre)',
      'phoenix (feat. alexa harley)',
      'hallucinate (feat. nevve)',
      'shrine (hex cougar remix) (feat. freya ridings)',
      'touch (feat. tiffani juno)',
      'you take my hand (feat. jamie irrepressible)',
      'lone [slow hours remix] (feat. joy.)',
      'you and me (feat. ke\'nekt)',
      'walk away (hibell remix) (feat. luna aura)',
      'don\'t worry (feat. ink)',
      'here and now (holding on) (feat. francis skyes)',
      'take it all (feat. blush\'ko)',
      'forever (feat. broods)',
      'ain\'t nobody (loves me better) (feat. jasmine thompson)',
      'stay in love (arrient remix) (feat. ofelia)',
      'stay in love (last island remix) (feat. ofelia)',
      'fallss (gigamesh remix)',
      'faces (feat. luma)',
      'go big (from "coming 2 america") (feat. big sean)',
      'goddess (feat. raja kumari)'
   ]:
      continue
   # tit = urllib.parse.quote(ytrack['title']).lower()
   ref = ytrack['artists'][0]['name']
   jprint(ytrack)
   print()
   print(tit)
   print()
   # ref = urllib.parse.quote(ref).lower()
   # print(ref)
   try:
      sps = sp.search(f'track:{tit} artist:{ref}', limit=5, offset=0, type='track', market=None)
   except SpotifyException:
      sps = sp.search(f'track:{tit}', limit=5, offset=0, type='track', market=None)
   if not len(sps['tracks']['items']): 
      try:
         sps = sp.search(f'track:{tit}', limit=5, offset=0, type='track', market=None)
      except SpotifyException:
         pass

      if not len(sps['tracks']['items']): 
         print('Not found')
         input('Continue?')
   ysids = [i['id'] for i in sps['tracks']['items']]
   cunt = False
   
   trkd = False
   for i in ysids:
      if i in ytks:
         cunt = True #!rm
         # mem.move(None, ypid['id'], mem.diff([sps['tracks']['items'][int(idx)]['id']], ytks))
         if i not in mem.sids:
            #TODO - remixes?
            pass
         # break
      elif i in mem.sids:
         cunt = True #!rm
         mem.move(None, ypid['id'], mem.diff([i], ytks))
         ytks.append(i)
         # break
   if not cunt:
      if len(sps['tracks']['items']) == 1:
         mem.move(None, SAVED, [sps['tracks']['items'][0]['id']])
         mem.move(None, ypid['id'], [sps['tracks']['items'][0]['id']])
      else: #! detect removal instead
         jprint([[i['id'], i['name'], ', '.join([j['name'] for j in i['artists']])] for i in sps['tracks']['items']])
         while not idx:#.isdigit():
            idx = input('?: ')
            if not idx: break
            inds = idx.split(" ")
            for item in inds:
               if not item.isdigit():
                  idx = ''
                  break
            for item in inds:
               mem.move(None, SAVED, [sps['tracks']['items'][int(item)]['id']])
               mem.move(None, ypid['id'], [sps['tracks']['items'][int(item)]['id']])
         if not idx: continue #! auto add remixes
      