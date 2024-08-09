from _base import *
import pydash as _

"""TODO
- nost integration
- add cache back in
- unheard respect - add to reduce -> rm.py
- ytm unheard, search, sycning
- reduce overlapping with untracked cache
- daily mixes
"""

def pullPi():
   print('TODO: pullPi')
   return

sids = mem.sids
ids_cache = mem.get_track_ids(p_cache)
untrack = mem.diff(mem.sids, ids_cache)
def sync():
   global untrack, sids
   """
   Check for unsaved 
   """
   while not mem.sids: #scheduler
      continue #async

   print("Syncing in Genres...")

   for gen in spotify_genres:
      p = mem.pname(f'{gen} Mix')
      ids_p = mem.get_track_ids(p)
      own = mem.pname(gen)
      ids_own = mem.get_track_ids(own)

      #saved
      new = mem.intersect(sids, ids_p)
      new = mem.diff(new, ids_own)
      if len(new):
         mem.move(None, own['id'], new)

      # reduce
      tmp = mem.diff(ids_p, [*heard])
      tmp = mem.diff(tmp, ids_own)
      tmp = mem.diff(tmp, new)
      tmp = mem.diff(tmp, mem.get_track_ids(p_red))
      if len(tmp):
         mem.move(None, p_red['id'], tmp)

      
      #cache syncing
      ovr = mem.intersect(ids_own, ids_cache)
      if len(ovr):
         mem.move(p_cache['id'], None, ovr)
      untrack = mem.diff(untrack, ids_own)
      
      ovr = mem.diff(new, ids_cache)
      if len(ovr):
         mem.move(p_cache['id'], None, ovr)
      untrack = mem.diff(untrack, new)

   print('UNTRACKED: ', len(untrack))
   return

def removeOutDated(base_trks, days=31): #! to file remove from spotify algorithm
   """
   Remove two week old tracks from saved
   """
   
   cutoff = (datetime.now() - timedelta(days=days)).timestamp()
   # tracks = [s['added_at'] for s in mem.saved]
   # tracks = list(map(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ').timestamp(), tracks))
   # tracks = list(map(lambda x: x < cutoff, tracks))
   lst = []
   for s in base_trks:
      if datetime.strptime(s['added_at'], '%Y-%m-%dT%H:%M:%SZ').timestamp() < cutoff:
         lst.append(s['track']['id'])
   return lst


def removeOutDatedReduce():
   trks = mem.retrieve(TRACK, pid=p_red['id'])
   print(len(trks))
   lst = removeOutDated(trks)
   print("REDUCING: ", len(lst))

   for t in lst:
      heard[t] = datetime.now().timestamp()
   
   with open(fn, 'w') as f:
      json.dump(heard, f)

   mem.move(p_red['id'], None, lst)

def removeOutDatedSaved(): #! to file remove from spotify algorithm
   global sids, ids_cache, untrack
   lst = removeOutDated(mem.saved)
   new = mem.diff(untrack, ids_cache)

   assert len(new) == len(untrack)
   
   print('OLD :', len(lst))
   print('MOVE:', len(new))

   mem.move(None, p_cache['id'], new) #! all saved not just outdated
   mem.move(SAVED, None, lst)
   # moving should match last number

def cleanUnheard():
   return

def autoDedup():
   return

def findUnheard():
   return

def find_remixes():

   #remove after 2 weeks
   return

def fctn():
   """
   """

   return


#! pocketbase py

def listen():
   last = 'nope'

   p = p_red

   lst = mem.get_track_ids(p)
   seek = False
   # lk = {}
   count = 0

   unhear = True
   devices = sp.devices()

   device = '08678dc3a932be320dbf9cea43c725cadd011898' #phone
   #device = '91843507fc92e427f86ddf0674968629d6e75237' #m1

   mem.move(p['id'], None, mem.sids)

   while 1:
      res = sp.currently_playing()
      prog = res['progress_ms']
      t = res['item']
      sid = t['id']
      if unhear:
         if sid in [*heard]:
            sp.next_track()
            sleep(1)
            continue
      if seek:
         if not count%3:
            sp.seek_track(prog + 20000)
         count += 1
         print(count)
      # try:
      #    if count == 15:
      #       sp.next_track()
      # except spotipy.exceptions.SpotifyException:
      #    pass
      if last != sid:
         heard[last] = datetime.now().timestamp()
         with open(fn, 'w') as f:
            json.dump(heard, f)

         if seek:
            count = 0
         future = e.submit(sp.artists, [a['id'] for a in t['artists']])
         os.system('clear')
         
         if last in lst:
            mem.move(p['id'], None, [last])
            # print('Removed')
         artists = future.result()['artists']
         print(', '.join([a['name'] for a in artists]), ' - ', t['name'])
         genres = list(set(_.flatten([a['genres'] for a in artists])))
         print(genres)
         last = sid
         print()
         
         # jprint(devices)


      sleep(2)


if __name__ == '__main__':
   pullPi()
   sync()
   removeOutDatedSaved()
   removeOutDatedReduce()

   listen()