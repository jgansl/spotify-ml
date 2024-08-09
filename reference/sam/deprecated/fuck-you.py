import concurrent.futures

from datetime import datetime, timedelta
# from pydash import flatten
from random import shuffle

from _constants import *
from _functions import *
from _utilities import *

def rmCacheFromLiked():
   global cycle
   print('\n\nrmCacheFromLiked')

   cache = getPlaylist('Cache')
   cache_track_ids = []#[t['track']['id'] for t in retrieve(TRACK, pid=cache.sid)]
   for t in retrieve(TRACK, pid=cache.sid):
      try:
         cache_track_ids.append(t['track']['id'])
      except:
         continue

   if len(cache_track_ids):
      #! TODO 
      move(SAVED, None, cache_track_ids) #! diff only
      move(cycle.sid, None, cache_track_ids)

def rmMemoriesFromLiked():
   global cycle
   print('\n\nrmMemoriesFromLiked')

   cycle_track_ids = []
   for t in retrieve(TRACK, pid=cycle.sid):
      try:
         cycle_track_ids.append(t['track']['id'])
      except:
         continue
   print(len(cycle_track_ids))

   for p in [ #!previous playlist names - June Electric Forest; #! tag--year tag--memories
      '2024',
      '2023',
      '2022',
      '2021',
      '2020',
      '10s',
      '00s',
      '90s',
      '80s',
      'Mom',
      'Dad',
   ]:
      p = getPlaylist(p)
      p_track_ids = []#[t['track']['id'] for t in retrieve(TRACK, pid=p.sid)]
      for t in retrieve(TRACK, pid=p.sid):
         try:
            p_track_ids.append(t['track']['id'])
         except:
            continue
      lst = list(set(p_track_ids).intersection(set(cycle_track_ids))) # less requests
      move(SAVED, None, lst)
      move(cycle.sid, None, lst)

   return

def cycleLiked():
   global cycle, today, now
   print('\n\ncycleLiked')

   liked = retrieve(SAVED)
   # liked_ids = [t['track']['id'] for t in retrieve(SAVED)]
   lst = []
   days = 14
   cutoff = (now - timedelta(days=days)).timestamp()
   for track in liked:
      if datetime.strptime(track['added_at'], '%Y-%m-%dT%H:%M:%SZ').timestamp() < cutoff:
         lst.append(track['track']['id'])
   #print(len(lst))

   # cycle = getPlaylist('Cycle')
   cycle_track_ids = [t['track']['id'] for t in retrieve(TRACK, pid=cycle.sid)]
   
   tmp = list(set(lst).difference(set(cycle_track_ids)))
   print('Cycling out:', len(tmp))
   if len(tmp):
      move(None, cycle.sid, tmp)
   if len(lst):
      move(SAVED, None, lst)
   sleep(3)
   
   cycle_tracks = retrieve(TRACK, pid=cycle.sid)
   shuffle(cycle_tracks)
   amt = int(len(cycle_tracks) / 25)
   print('Cycling in:', amt)
   # move( None, SAVED, lst)
   #! remove those that are less than 10 minutes old; currently only add the oldest 10 percent
   # for c in cycle_tracks[:amt]:
   #    print(c['added_at'])
   cycling = [t['track']['id'] for t in cycle_tracks[:amt]]
   move(cycle.sid, SAVED, cycling)
   sleep(3)
   move(None, cycle.sid, cycling)

   
   return


if __name__ == '__main__':
   cycle = getPlaylist('Cycle')
   now = datetime.now()
   today = '2024-02-20' #! UTC; run then update


   if False: # developing
      
      pass # prd daily
   else:
      #... not working 2023 still in cycle
      rmCacheFromLiked() # move songs older than 2 years from cycle?
      rmMemoriesFromLiked()


      if today in str(datetime.now().date()): #! only once per day
         
         cycleLiked() #genre
      
      # scanInTracks() #implicitly scan in artists
      # patchDB()
      # scanInArtists()

   pass 
