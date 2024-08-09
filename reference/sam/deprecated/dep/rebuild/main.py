"""
AI refactoring; singletons, and caching

implicit playlist following
development account; backup and restore
years - remove cache into single collection of multiple genres
"""

from functions import *
from datetime import datetime, timedelta
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
#TODO rm
from _sam import sam, PLAYLIST, SAVED, TRACK, sp, usr, SCOPE, TRACK

# from pocketbase import PocketBase
# from pocketbase.client import ClientResponseError
# pb = PocketBase('http://127.0.0.1:8092', 'en-US')


def weekly():
   def onRepeat():
      return

   def move():
      return
   

   return

def daily():
   def newReleases():
      return
   
   def rmFromLikedSongs():
      global saved
      saved_lookup = {}
      for s in sam.saved:
         saved_lookup[s['track']['id']] = s
      
      chill = sam.pname('Chill')
      chill_ids = sam.get_track_ids(chill)

      def funct(genre):
         # global db_artists_ids, db_artists_map
         global removable_sids
         print(genre)

         mix = sam.pname(genre + ' Mix')
         if not mix: return #continue #misnamed
         mix_ids = sam.get_track_ids(mix)
         if not len(mix_ids): return #continue #not followed

         collection = sam.pname(genre)
         collection_ids = sam.get_track_ids(collection)
         
         lst = sam.diff(sam.intersect(mix_ids, sam.sids), collection_ids)
         if len(lst): #TODO cross genres on2
            # print('moving ' + str(len(lst)) + ' tracks from ' + mix['name'] + ' to ' + collection['name'])
            sam.move(None, collection['id'], lst)
            collection_ids.extend(lst)
         sam.move(SAVED, None, sam.intersect(collection_ids, removable_sids))
            # for tid in lst:
            #    t = saved_lookup[tid]
            #    tmp2 = datetime.strptime( t['added_at'], '%Y-%m-%dT%H:%M:%SZ')
            #    tmp3 = today - tmp2
            #    if( tmp3.days > 14):
            #       sam.move(SAVED, None, [tid])
         
         
            ## Chill - #TODO Dance Pop, Indie Pop, Acoustic -> Folk & Acoustic
         if 'Chill' not in genre:
            chill_genre = sam.pname('Chill ' + genre)
            chill_genre_ids = sam.get_track_ids(chill_genre)

            ints = sam.intersect(chill_ids, collection_ids)
            lst = sam.diff(ints, chill_genre_ids)
            if len(lst):
               sam.move(None, chill_genre['id'], lst)
            if len(ints):
               sam.move(collection['id'], None, ints)


         
         return

      genres_list = [ #TODO implicitly follow
         # 'Anti Anxiety',
         'Party',
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
         'Workout EDM',
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
      # for genre in genres_list:
      #    funct( genre )
      with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
         # Start the load operations and mark each future with its URL
         future_to_genre = {executor.submit(funct, genre): genre for genre in genres_list}
         for future in concurrent.futures.as_completed(future_to_genre):
            genre = future_to_genre[future]
            try:
               data = future.result()
            except Exception as exc:
               print('%r generated an exception: %s' % (genre, exc))
      
      print('done rmFromLikedSongs')
      return
   rmFromLikedSongs()
   print('done daily')

if __name__ == '__main__':
   OWNED = [p for p in sam.playlists if p['owner']['id'] == usr]

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

      if( tmp3.days >= 14 or tmp3.days > 7 and released.days > 30):
         removable_sids.append(s['track']['id'])
   print(len(removable_sids))
   # exit()
   weekly()
   daily()

   print('done')
