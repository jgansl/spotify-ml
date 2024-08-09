## plan of changes - stable updating; site coloring
# testing environment; account; youtube syncing
# test before continuing - ensure nondestructive
# manually update artists - for now
#TODO update listen to correctly pull and organize; operate
#TODO cycles
#TODO - exclusion sopecifications
#TODO - tagging
# how to berak and dissovlev "Chill" into "Meloncolhy etc." -channeling?
# use artists to organize Daily Mix new songs 
# - GOAL:independent of packetbase DB - internalize playlist following; potential loss of data source

from base import *
from sam import sam, PLAYLIST, SAVED, TRACK, sp, usr, SCOPE, TRACK
from datetime import datetime, timedelta

MIXES = [ # remove from liked #TODO one at a time - exclude
   # 'Anti Anxiety', #true #TODO not capturing all in saved
   # 'Alternative', #true
   # 'Alt Z', #true
   # 'Angry', #true
   # 'Aussietronica', #true
   'Beach',
   # 'Chill', #false
   # 'Chillwave', #false
   # 'Cyberpunk',
   # 'Dance/Electronic', #false
   # 'Drum and Bass', #true
   # 'Dubstep', #true
   # 'Euphoric',
   # 'Folk & Acoustic', #true
   # 'Futurepop', #true
   # 'Hip Hop', #false
   # 'House', #false -calm #true
   # 'Indie', #false -calm #true
   # 'Lit Shower', #false -calm #true
   # 'Moody', #false -calm #true
   # 'Pop', #true
   # 'Pump Up', #true
   # 'Punk',
   # 'Rock', #true
   # 'R&B', #true
   # # 'Vaporwave', #true
   # 'Vapor Soul', #true
   # 'Vapor Twitch', #true

]
GENRE_PLAYLIST_CHANNELING = {
   'Tranquil': 'Chill Mix',
   'Chill': 'Chill Mix',
   # 'Indie pop': 'Indie/Pop',
   'Rap Mix': 'Hip Hop Mix',
   #! not a spotify genre in search - serach for 'Rap' -> hop hop genre
   # 'Alternative hip hop': 'Hip Hop',
   'Alternative hip Hop Rap Mix': 'Hip Hop Mix',
   'Acoustic': 'Folk & Acoustic Mix',
}

TAGS = [
   'genre-artists',
   'genre-cache',
   'genre-new',
   'memories',
]

RESERVED = [
   'cache',
   'tracks',
   't'
]

def func():

   return


def func2():
   'remove mixes -true from liked songs'

   return

def func1(): #TODO TEST; tags; TODO cross genre
   """
   for now, removes from liked songs (reduce cache) -> if specified; 
   """
   global MIXES

   pcache = sam.pname('Cache')
   pcache_ids = sam.get_track_ids(sam.pname('Cache'))


   # get personal playlist - create and add description is not present - tmp rename
   for genre in MIXES:
      print(genre)
      mix = sam.pname(genre + ' Mix')
      # combine for tracks
      collection = sam.pname(genre)
      collection_ids = sam.get_track_ids(collection)
      tracks = collection_ids
      cache = sam.pname('Cache - '+genre, description='#genre-cache')
      cache_ids = sam.get_track_ids(cache)
      tracks.extend(cache_ids)
      # TODO collection recommendations -> add instaed to general playlist
      new = sam.pname('New - '+genre, description='#genre-new')
      artists = sam.pname('Artists - '+genre, description='#genre-artists')
   
      # find intersect songs
      mix_ids = sam.get_track_ids(mix)
      coll_tracks = sam.intersect(mix_ids, pcache_ids)#TODO sam.sids)
      diff = sam.diff(coll_tracks, tracks)
      sam.move(None, collection['id'], diff)
      tracks.extend(diff)
      for i in [new, artists]:
         tracks.extend(sam.get_track_ids(i))
      new_tracks = sam.diff(mix_ids, tracks)
      sam.move(None, new['id'], new_tracks)
      #remove liked songs just added to collection
      tracks.extend(sam.get_track_ids(mix)) 
      #TODO -> rm from cached below...NEVERMIND; WORKAROUND
      # # sam.move(SAVED, None, tracks)# - song added to muliptle genres - before tagging is added, instaed remove after 1 month
      
      #TODO mve new into collection

      # split into old and new
      # -grab all songs
      # -inter and non-inter
      
      # add to respective playlists - exclude cache, new-artists
      # Liked/Cache - [GENRE] - #genre-cache
      # move old into cache, remove cache from current
      # New Artists - [GENRE] - #new-artists
      # move unheard into new

      # move old songs into cache - check one a year
      #- remove collection from new; #TODO remove after 3 months
      #- remove cache from new - not often
      #- remove cache from collection - not often
      tmp = sam.retrieve(TRACK, pid=collection['id'])
      for t in tmp:
         print('\t'+t['track']['name'])
         #TODO remove from new
         sam.move(new['id'], None, [t['track']['id']])
         if t['track']['album']['release_date'] < '2023':
            if t['track']['id'] not in cache_ids:
               sam.move(collection['id'], cache['id'], [t['track']['id']])
               #tmp rm from liked songs
               # # sam.move(SAVED, None, [t['track']['id']])
            else:
               sam.move(collection['id'], None, [t['track']['id']])
               #tmp rm from liked songs
               # # sam.move(SAVED, None, [t['track']['id']])

      # NOTE: ONLY REMOVES THOSE TRACKED; AND MIXES THEM
      for t in sam.retrieve(TRACK, pid=cache['id']):
         print('\t'+t['track']['name'])
         sam.move(new['id'], None, [t['track']['id']])
         # tmp1 = datetime.now()
         # tmp2 = datetime.strptime(
         #    t['added_at'], #@see https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
         #    #2023-08-08T22:28:17Z
         #    # '%d/%m/%y %H:%M:%S.%f')
         #    '%Y-%m-%dT%H:%M:%SZ')
         # tmp3 = tmp1 - tmp2
         # # print(type(tmp3))
         # # print(tmp3)
         # if( tmp3.days > 30): #TODO 31- let accum for a bit
         
         # sam.move(SAVED, None, [t['track']['id']])
         sam.move(pcache['id'], None, [t['track']['id']])
      
      # remove manually added from cache - TODO after 30 days 
      # sam.move(SAVED, None, mem.intersect(mem.get_track_ids(pcache), mem.sids))
      sam.move(pcache['id'], None, sam.intersect(sam.get_track_ids(pcache), sam.get_track_ids(cache)))
   return

# Youttube, smart shuffle
# TODO randomly cycle; add in old songs - but that is what spoitify is for
if __name__ == '__main__':
   func1()
