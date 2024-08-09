from ___sam import *
import re
from concurrent.futures import ThreadPoolExecutor
e = ThreadPoolExecutor(max_workers=5)
jprint = lambda x: print(json.dumps(x,indent=2))

mem = SAM(sp)
cache =  mem.pname('CacheX')
nost =  mem.pname('Nostalgia') #TODO
radio_mixes = [p for p in mem.playlists if 'Mix' in p['name'] or 'Radio' in p['name']]
unowned = [p for p in mem.playlists if p['owner']['id'] != usr]
colls = [p for p in mem.playlists if '.collection' in p['description']]

def cacheSaved():
   global cache
   mem.move(None, cache['id'], mem.diff(mem.sids, mem.get_track_ids(cache)))
   # remove 30 day old tracks
   cache_ids = mem.get_track_ids(cache)

   for p in radio_mixes: #TODO ignore artists
      nm = re.sub('( Radio| Mix)', '', p['name'])
      if nm not in [
         'Blues',
         'Chill',
         'Dance/Electronic',
         'Drum and Bass',
         'Folk & Acoustic',
         'Hip Hop',
         'House',
         'Indie',
         'Pop',
         'R&B',
         
         '2010s',
         '2000s',
         '90s',
         '80s',
         '70s',
         
         'Gorgon City',
         'Goth Babe',
         'Lane 8',
         'Hippe Sabotage',
         'Dance Rising'
      ]:
         print('Skipping ' + nm)
         continue
      pn = mem.pname(nm)
      p_tids = mem.get_track_ids(pn)
      mov_tids = mem.diff(p_tids, mem.intersect(cache_ids, p_tids))
      mem.move(cache['id'], pn['id'], mov_tids)
      mem.move(cache['id'], None, mem.intersect(cache_ids, p_tids))

   for p in colls:
      mem.move(SAVED, None, mem.intersect(mem.get_track_ids(p), mem.sids))
      mem.move(cache['id'], None, mem.intersect(mem.get_track_ids(p), cache_ids))
      pass

def autoSortCache():
   #ml - attributes
   return

def unheard():

   return

if __name__ == '__main__':
   cacheSaved()