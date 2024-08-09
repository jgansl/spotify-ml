from os import system
from time import sleep
import json
from datetime import datetime, timedelta
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor as PoolExecutor

# from _constants import (
#    SCOPE, 
#    PLAYLIST,
#    SAVED,
#    TRACK
# )

from sam import sam, PLAYLIST, SAVED, TRACK, sp, usr, SCOPE, TRACK


def patch1():
   for i in [
      'Anti Anxiety',
      'Alternative',
      'Alt Z',
      'Angry',
      'Aussietronica',
      'Beach',
      'Blues',
      'Chill',
      'Chillwave',
      'Cyberpunk',
      'Dance/Electronic',
      'Drum and Bass',
      'Dubstep',
      'Euphoric',
      'Folk & Acoustic',
      'Futurepop',
      'Hip Hop',
      'House',
      'Indie',
      'Lit Shower',
      'Moody',
      'Pop',
      'Pump Up',
      'Punk',
      'Rock',
      'R&B',
      'Singing',
      # 'Vaporwave',
      'Vapor Soul', #true
      'Vapor Twitch', #true
   ]:
      playlist_id = sam.pname('Cache - '+i)
      sam.move(playlist_id['id'], sam.pname(i)['id'], sam.get_track_ids(playlist_id))
      sp.current_user_unfollow_playlist(playlist_id['id'])
      playlist_id = sam.pname('Artists - '+i)['id']
      sp.current_user_unfollow_playlist(playlist_id)
      playlist_id = sam.pname('New - '+i)['id']
      sp.current_user_unfollow_playlist(playlist_id)
   return
patch1()