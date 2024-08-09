# import concurrent.futures

from _constants import SAVED, TRACK
from _functions import retrieve, move, pname
# from _utilities import *


def patch():
   p = pname('Always Rising')
   lst = [s['track']['id'] for s in retrieve(TRACK, pid=p['id'])]
   saved = retrieve(SAVED)
   sids = [s['track']['id'] for s in saved]
   move(SAVED, None, list(set(sids).intersection(set(lst))))
   cycle = pname('Cycle')
   cycle_ids = [s['track']['id'] for s in retrieve(TRACK, pid=cycle['id'])]
   move(cycle['id'], None, list(set(cycle_ids).intersection(set(lst))))
patch()



#
#
#


def fillMissingData():
   return #! TODO

def patchArtistsPopularity(): #! followers
   for artist in db_artists:
      data = sp.artist(artist.spotify_id)
      pb.collection('artists').update(
         artist.id,
         {
            "popularity": data['popularity'], #TODO changes?; 0-100
            "followers": data['followers']['total'], #TODO update
         }
      )
   return

def patchHeard():
   for t in db_heard:
      track = sp.track(t.spotify_id)
      track = {'track': track}
      print(track['track']['name'], track['track']['artists'][0]['name'])
      try:
         addHeardToArtists(track)
      except: continue
      pb.collection('heard').delete(t.id)

   return
def patchPlaylistHeard():
   # for track in retrieve(TRACK, pid=playlist['id'])[:5]:
   def func(track):
      # print(track['track']['id'])
      addHeardToArtists(track)
      return track['track']['name']
   for playlist in [p for p in playlists() if p['owner']['id'] == usr]:
      # We can use a with statement to ensure threads are cleaned up promptly
      with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
         # Start the load operations and mark each future with its URL
         future_to_url = {executor.submit(func, t): t for t in retrieve(TRACK, pid=playlist['id'])}
         for future in concurrent.futures.as_completed(future_to_url):
            anme = future_to_url[future]
            try:
               data = future.result()
            except Exception as exc:
               print('ERROR', anme)#%r generated an exception: %s' % (name, exc))
            else:
               print(data)
      sleep(3)
   return