import json
from _sam import SAM, usr, sp

jprint = lambda x: print(json.dumps(x, indent=4))

sam = SAM()

personal = [p for p in sam.playlists if p['owner']['id'] == usr]
cache = sam.pname('Cache hidden')
cache_track_ids = sam.get_track_ids(cache)


exit()


for p in personal:
   if(p['name'] == 'Cache hidden'):
      continue
   track_ids = sam.diff(sam.get_track_ids(p), cache_track_ids)
   if len(track_ids):
      cache_track_ids.extend(track_ids)
      print(len(track_ids), len(cache_track_ids))
      sam.move(None, cache['id'], track_ids)
   sp.current_user_unfollow_playlist(p['id'])
