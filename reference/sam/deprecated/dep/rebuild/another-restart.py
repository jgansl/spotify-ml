# KISS , functional, no more than ten lines per function
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

from _sam import sam, PLAYLIST, SAVED, TRACK, sp, usr, SCOPE, TRACK

jprint = lambda x: print(json.dumps(x, indent=4))

import pocketbase
from pocketbase import PocketBase
from pocketbase.client import ClientResponseError
pb = PocketBase('http://127.0.0.1:8092', 'en-US')
TABLE_PLAYLISTS = pb.collection('playlists')

# dance playlist that contains all new dance/electronic removed after a certain amount of time, cached if saved

# all controlled thorugh spotify, aid though pocketabse

SPOTIFY_CHANNELS = {
   'New': [
      'Daily Mix 1',
      'Daily Mix 2',
      'Daily Mix 3',
      'Daily Mix 4',
      'Daily Mix 5',
      'Daily Mix 6',
      'Monday Mix',
      'Tuesday Mix',
      'Thursday Mix',
      'Friday Mix',
      'Saturday Mix',
      'Sunday Mix',
      'Discover Weekly', # TODO multiple
      'Release Radar',
      'Fresh Mix',
      'New Music Friday',
      'New Music Now',
      'Selected. Releases',
      'HITS 2023 - Today\'s Top Hits',
      'Top 50 - Global',
      'Top 50 - USA',
      'Wild & Free',
      'young & free',
      'Summer Party'
      'Party Hits'
   ],
   'Dance/Electronic': [
      "Bass Lounge",
      "EDM Hits",
      'New Music Friday Dance',
   ],
   'House': [
      'Progressive Deep House',
      'Progressive House Mixes',
      # 'Stutter House 2023'
      'Stutter EDM'
   ],
   'R&B': [
      'R&B Right Now',
      'R&B Weekly',
   ]
}

RADIO_CHANNELS = {

}

DAILY_CHANNELS = {

}

WEEKLY_CHANNELS = {

}

SUBGENRES_CHANNELS = {

}

#! new playlist
#! remove into years
GENRES = [ #TODO implicitly follow
   # 'Anti Anxiety',
   'Alternative',
   'Alternative Pop',
   'Alt Z',
   'Angry',
   'Aussietronica',
   'Beach',
   'Blues',
   'Brostep',
   'Chill',
   'Chillwave',
   'Country',
   'Classy',
   'Classic Rock',
   'Moody Soft',
   'Soft',
   'Cyberpunk',
   'Bass EDM',
   'Dance EDM',
   'Hype EDM',
   # 'Workout EDM',
   'Party',
   # 'EDM',
   'Dance House',
   'Dance Pop',
   'Indie Dance',
   'Indie ElectroPop',
   'Dance/Electronic',
   'Drum and Bass',
   'Dubstep',
   'Euphoric',
   'Folk & Acoustic',
   'Chill Future Bass',
   'Future Bass',
   'Futurepop',
   'Hip Hop',
   'Chill Hip Hop',
   'Hardstyle',
   'House',
   'Indie',
   'Lit Shower',
   'Moody',
   'Party',
   'Pop Dance',
   'Pop EDM',
   'Pop',
   'Pump Up',
   'Punk',
   'Rock',
   'R&B',
   'Singing',
   'Soul',
   # 'Stutter House',
   'Soulful R&B',
   'Trap',
   # 'Vaporwave',
   'Vapor Soul', #true
   'Vapor Twitch', #true
   'Witchcore'
]

# sync playlists with pocketbase - restoration

class xSAM(): # make all edits locally and then sync? - redis local copy to eventually sync

   # self.playlists = {
   #    # 'id': 
   #    # 'name':
   #    # 'description':
   #    # 'tracks':
   # }

   def __init__(self):

      return
   
   def move(self, src, dst):
      # keep memory cache

      return

def cacheYears():
   # if in genre, remove year

   def funct(s, pid=SAVED):
      track_year = int(s['track']['album']['release_date'][:4])
      # if track_year <= datetime.now().year:
      if s['track']['id'] in removable_sids:
         if track_year < 1980:
            playlistname = '70s'
         if track_year < 1990:
            playlistname = '80s'
         if track_year < 2000:
            playlistname = '90s'
         else:
            playlistname = str(track_year)
         p_year = sam.pname(playlistname)
         sam.move(
            None, # SAVED, 
            # prevent duplicates
            p_year['id'], 
            sam.diff(
               [
                  s['track']['id']
               ], 
               mem.get_track_ids(p_year)
            )
         )
      
      # move to genre if in removeable
      # remove old from genres

      # print(track_year)
      # if track_year < datetime.now().year: #-1 200; but heard in 2023 #added in 2023; after 2 weeks
      #    if pid != SAVED or s['track']['id'] in removable_sids:
      #       sam.move(
      #          pid, 
      #          None, 
      #          # TODO non-duplicate
      #          [
      #             s['track']['id']
      #          ]
      #       )
      # else:
      #    if pid != SAVED:
      #       sam.move(
      #          pid, 
      #          SAVED, 
      #          # TODO non-duplicate
      #          [
      #             s['track']['id']
      #          ]
      #       )


      #    lst.append(s['track']['id'])
   

   # for s in sam.saved:
   with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
      # Start the load operations and mark each future with its URL
         future_to_s = {executor.submit(funct, s): s for s in sam.saved}
         for future in concurrent.futures.as_completed(future_to_s):
            s = future_to_s[future]
            try:
               data = future.result()
            except Exception as exc:
               print('%r generated an exception: %s' % (s, exc))
   
   
   # for g in GENRES:
   #    print(g)
   #    p = sam.pname(g)
   #    pid = p['id']
   #    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
   #       # Start the load operations and mark each future with its URL
   #          future_to_s = {executor.submit(funct, s, pid): s for s in sam.retrieve(TRACK, pid=pid)}
   #          for future in concurrent.futures.as_completed(future_to_s):
   #             s = future_to_s[future]
   #             try:
   #                data = future.result()
   #             except Exception as exc:
   #                print('%r generated an exception: %s' % (s, exc))
   #    sp.current_user_unfollow_playlist(pid)


   return

def get_removable_sids(max_days=14):
   removable_sids = []
   today = datetime.now()
   for s in sam.saved:
      tmp2 = datetime.strptime(
         s['added_at'], #@see https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
         #2023-08-08T22:28:17Z
         # '%d/%m/%y %H:%M:%S.%f')
         '%Y-%m-%dT%H:%M:%SZ')
      tmp3 = today - tmp2
      # print( s['track']['name'], tmp3.days)
      # print(type(tmp3))
      # print(tmp3)

      # release date
      release_date = s['track']['album']['release_date']
      if not release_date :
         continue
      # else: print(release_date)
      
      len_release_date = len(release_date)
      if len_release_date == 4: #year
         print( release_date )
         release_date = datetime.strptime(
            release_date,
            '%Y'
         )
         print( release_date )
         print()
      elif len_release_date == 10:
         release_date = datetime.strptime(
            release_date,
            '%Y-%m-%d'
         )
      else:
         print('INVALID RELEASE DATE Processing')
         input(s['track']['album']['release_date'])

      released = today - release_date
      # print( released.days)
      # print()

      if( tmp3.days >= max_days or tmp3.days > 7 and released.days > 30):
         removable_sids.append(s['track']['id'])
   print(len(removable_sids))
   sleep(1)
   return removable_sids


def newtracks(): #! NEXT

   for p in [
      'Daily Mix 1',
      'Daily Mix 2',
      'Daily Mix 3',
      'Daily Mix 4',
      'Daily Mix 5',
      'Daily Mix 6',
      'Release Radar', #multiple
      'Discover Weekly'
   ]: 
      # get tracks
      # pocketbase check against
      # add to new playlist
      # categorize by artist - pb artist unheard
      pass

if __name__ == '__main__':
   # copy all songs to liked songs
   # remove years and build generes
   # privateize and refolder
   # remove years from genres and build genres
   removable_sids = get_removable_sids(14)
   cacheYears() #! TODO move into 2023 (logic?), remove playlist from liked
   # remove because already in year vs remove because it was a 2023 hit?
   # assume first, add manually later

   # manually remove from saved
   # scan artists for news songs 
   # functional and time tested; cache
   
   # MASS Control
   # playlist table
   # artist table
   # unheard in artists -> genre new

   # queue new songs only - genre - chozen, http://organizeyourmusic.playlistmachinery.com/# smart shuffle



   pass