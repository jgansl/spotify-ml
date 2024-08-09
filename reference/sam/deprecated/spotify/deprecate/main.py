from base import *
import pydash as _

"""CONVERSION PHASES
- reduce caches
- daily artist

"""

reserved = [ 'tid', 's', 'lst', 'sid', 'trk', ]

def co(
   fctn,
   lst=[],
   max_workers=5
):
   with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
      future_to_url = {executor.submit(fctn, item): item for item in lst}
      for future in concurrent.futures.as_completed(future_to_url):
         url = future_to_url[future]
         try:
               data = future.result()
         except Exception as exc:
               print('%r generated an exception: %s' % (url, exc))
         else:
               print('%r page is %d bytes' % (url, len(data)))

def tmp():
   p = mem.pname('Cache 0')
   trks = mem.get_track_ids(p)


   def fctn():
      """
      """

      return

   with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
      future_to_url = {executor.submit(fctn, url, 60): tid for tid in trks}
      for future in concurrent.futures.as_completed(future_to_url):
         url = future_to_url[future]
         try:
               data = future.result()
         except Exception as exc:
               print('%r generated an exception: %s' % (url, exc))
         else:
               print('%r page is %d bytes' % (url, len(data)))

   return

def setupCache():
   fn = 'data/caches.json'
   if os.path.exists(fn):
      with open(fn, 'r') as f:
         caches = json.load(f)

         #! update reduce daily
   else:
      caches = [
         # 'Reduce',
         'Cache 0',
         'Cache 1',
         'Cache 2',
         'Cache 3',
         'Cache 4',
      ]
      caches = list(map(lambda x: mem.pname(x), caches)) #memo
      with open(fn, 'w') as f:
         json.dump(caches, f, indent=2)

   fn = 'data/lookup_caches.json'
   if os.path.exists(fn):
      with open(fn, 'r') as f:
         lookup_caches = json.load(f)
   else:
      lookup_caches = list(map(lambda x: mem.get_track_ids(x), caches))
      with open(fn, 'w') as f:
         json.dump(lookup_caches, f, indent=2)
   return (caches, lookup_caches)

(caches, lookup_caches) = setupCache()
last = None
def listen():
   global last
   
   seek = True
   count = 0

   # devices = sp.devices()
   device = '08678dc3a932be320dbf9cea43c725cadd011898' #phone
   #device = '91843507fc92e427f86ddf0674968629d6e75237' #m1

   artists_lst = []
   afn = 'data/artists.json'
   if os.path.exists(afn):
      with open(afn) as f:
         artists_lst = json.load(f)
   while True:
      res = sp.currently_playing()
      if not res:
         print('Not Playing')
         sleep(2)

      prog = res['progress_ms']
      trk = res['item']
      sid = trk['id']

      if seek:
         if not count%2:
            sp.seek_track(prog + 15000)
         count += 1

      if last != sid:
         os.system('clear')
         if seek: count = 0
         
         for i in range(len(lookup_caches)):
            if sid in lookup_caches[i]:
               print(caches[i]['name'])
               mem.move(caches[i]['id'], None, [sid])
         
         future = e.submit(sp.artists, [a['id'] for a in trk['artists']])
         artists = future.result()['artists']
         artists_lst.extend([a['id'] for a in artists])
         artists_lst = list(set(artists_lst))
         with open(afn, 'w') as f:
            json.dump(artists_lst, f, indent=2)
         print(', '.join([a['name'] for a in artists]), ' - ', trk['name'])
         genres = list(set(_.flatten([a['genres'] for a in artists])))
         print(genres)


         last = sid
      
      sleep(3)

def sync():
   #remove saved from caches
   #remove untracked from caches
   #remove playlists from caches
   global lookup_caches, caches

   owned = [p for p in mem.playlists if p['owner']['id'] == usr]

   for p in owned:
      if 'Reduce' in p['name']:
         print('SKIP: ' + p['name'] )
         continue
      if 'Cache' in p['name']:
         print('SKIP: ' + p['name'] )
         continue

      trks=mem.get_track_ids(p)
      for i in range(len(lookup_caches)):
         ints = mem.intersect(lookup_caches[i], trks)
         print('removing ' + str(len(ints)) + " from " + caches[i]['name'])
         mem.move(caches[i]['id'], None, ints)
         mem.move(caches[i]['id'], None, mem.intersect(mem.sids, lookup_caches[i]))
      


if __name__ == '__main__':
   # sync()
   listen()