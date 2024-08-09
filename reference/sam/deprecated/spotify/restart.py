from base import *
from pydash import flatten
from re import sub
from concurrent.futures import ThreadPoolExecutor


obj = {}
fn= 'state_11_20_22.json'
if os.path.exists(fn):
   with open(fn, 'r') as f:
      obj = json.load(f)
p_art = mem.pname('Artists')
p_tids = mem.get_track_ids(p_art)
aids = []
for pid in [*obj]:#mem.playlists:
   p = obj[pid]
   if p['name'] == 'Artists': continue
   # obj[p['id']] = {
   #    "name": p['name'],
   #    "owner_id": p['owner']['id'],
   #    "description": p['description'],
   #    "tracks": mem.get_track_ids(p)
   # }
   for t in p['tracks']: #mem.retrieve(TRACK, pid=pid):
      t = sp.track(t)
      # jprint(t)
      if(t['artists']):
         sp.user_follow_artists([a['id'] for a in t['artists']])
   sleep(3)
      #! for a in t['track']['artists']:
         # if a['id'] not in aids:
         #    print(a['name'])
         #    for i in sp.artist_top_tracks(a['id'])['tracks']:
         #       if i['id'] not in p_tids:
         #          mem.move(None, p_art['id'], [i['id']])
         #          p_tids.append(i['id'])
         #    sleep(1)
   # with open(fn, 'w+') as f:
   #    json.dump(obj,f, indent=2)
   
   # sp.current_user_unfollow_playlist(p['id'])

#listen reduce -> 2 weeks