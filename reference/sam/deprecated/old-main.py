"""

New songs - only current year from daily mixes etc.
artist mixes - discover weekly - related artists
cycle cached into liked songs - 10 at a time - new cache
remove on repeat from liked songs into cache
remove any song that are from past years into cache
collections -> artists collections;
keep new at 100; remove after two weeks?
agile cycling of new songs
remove playlist songs from cache, liked, artist collections
radios? -> artists collections
on repeat - >cached
what should 
interface design


AI -> mojo
managed playlists - company royalty free
AI Artists
# move genres out after two weeks, if in genre remove, dont insert before
# new releases for artists in liked tracks?
# scan in daily mixes and only add new songs, remove after two weeks
# remove years, and genres from _cache
# daily artists mix; scan in artists
"""
from _constants import *
from _functions import *
from _utilities import *


def syncPlaylistsDescriptions(fromDB=False):
   return


def checkReleaseDate():
   return True

# old_saved_ids = []
# for s in saved:
#    if checkReleaseDate():
#       old_saved_ids.append(s)


db_tracks = [] 
device = None
def insertTrack(t):

   return
def scanInDailyMixes():
   for p in [ #implicitly follow
      'Daily Mix 1',
      'Daily Mix 2',
      'Daily Mix 3',
      'Daily Mix 4',
      'Daily Mix 5',
      'Daily Mix 6',
   ]:
      p = getPlaylist(p) #implicitly follow
      for t in retrieve(TRACK, pid=p['id']):
         if t not in db_tracks:
            print(t['track']['name'])
            insertTrack(t)
            if device:
               sp.add_to_queue()


   return

if __name__ == '__main__':

   if False:
      pass
   else:
      # does not scan in artists ye; new table
      scanInDailyMixes()
      
      # createDailyArtistMixes()

      pass
