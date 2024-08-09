from _base import *
import pydash as _
# e = ThreadPoolExecutor(max_workers=5)

#! pocketbase py

def listen():
   last = 'nope'
   p = p_red

   lst = mem.get_track_ids(p)
   seek = True
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
listen()
def try_this():
   # sp.recommendation
   return