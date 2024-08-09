from _constants import PUBLIC_PLAYLISTS
from _functions import playlists, sp, usr
from _db import sp_playlists
import concurrent.futures

def privatizePlaylists(): #! concurrently
   global PUBLIC_PLAYLISTS
   print('\nprivatizePlaylists')
   print(len([p for p in sp_playlists if p['owner']['id'] == usr]))
   
   # for p in playlists():
   def localFunc(p):
      if p['name'] not in PUBLIC_PLAYLISTS:
         sp.playlist_change_details(p['id'], public=False)
   #! generalize
   with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
      # Start the load operations and mark each future with its URL
      future_to_p = {executor.submit(localFunc, p): p for p in [p for p in sp_playlists if p['owner']['id'] == usr]}
      for future in concurrent.futures.as_completed(future_to_p):
         url = future_to_p[future]
         try:
            data = future.result()
         except Exception as exc:
            print('%r generated an exception: %s' % (p, exc))
         # else:
         #    print('%r page is %d bytes' % (p, len(data)))
   return