from _functions import *

#! Test Playlists; copies
#tag--test; pi
def copyPlaylist():

   return

# remove playlists tracks from cache
def patch():
   playlists = retrieve(PLAYLIST)
   cache = [p for p in playlists if p['name'] == 'Cache'][0]
   cache_tracks = [t['track']['id'] for t in retrieve(TRACK, pid=cache['id'])]
   print(len(cache_tracks))
   print(cache_tracks[:5])
   for p in playlists:
      if p['owner']['id'] not in usr or p['name'] == 'Cache':
         # print('Skipping ', p['name'])
         continue
      tracks = [t['track']['id'] for t in retrieve(TRACK, pid=p['id'])]
      lst = list(set(cache_tracks).intersection(set(tracks)))
      print(len(lst), p['name'], len(tracks))
      move(cache['id'], None, lst)

   return

# patch()

# add liked songs to cycle
def likedCycle():

   playlists = retrieve(PLAYLIST)

   return

likedCycle()


def higherSpecificity():
   pairs = [
      ['Dance/Electronic', 'Pop'],
   ]
   for p, q in pairs:
      pass