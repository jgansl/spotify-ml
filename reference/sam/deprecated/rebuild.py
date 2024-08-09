"""
- Minimize External Calls
"""
import concurrent.futures

from datetime import datetime
# from pydash import flatten
from os import system
from random import shuffle

# TODO remove depenedency; isolate this file
from _constants import *
from _functions import *
from _utilities import *
from daily import *

_followed_playlists = None #! manage locally
def getFollowedPlaylists(): #TODO cache - development; #TODO return records - getPlaylist
   global _followed_playlists
   if _followed_playlists:
      return _followed_playlists
   
   _followed_playlists = retrieve(PLAYLIST)
   return _followed_playlists

def newSyncPlaylistsToDB():
   global db_playlist_ids

   for p in getFollowedPlaylists():
      # if p['id'] not in db_playlist_ids:
      # print('sync playlist to DB:', p['name'])
      try:
         updatePlaylist(
            db_playlist_map[p['id']].id, 
            {
               'owner_name': p['owner']['display_name'],
            }
         )
      except KeyError:
         record = insertPlaylist(p)
   return

def insertTrackEntry(data, genre=None):#, table):
   if type(data) == str: #ID provided
      data = sp.track(data)
   else:
      data = data['track'] #! added_at

   #! if t['id'] not in db_track_ids:
   # print([*data])
   table = "tracks"
   try: 
      record = pb.collection(table).create(
         {
            "name": data['name'],
            "sid" : data['id'],
            'genres': [],
            'release_date': data['album']['release_date'],
            'artists': [a['id'] for a in data['artists']],
            'new': True,
            'liked': False,
            # 'cached': False,
            "specificity": 1,
            "spotify_id" : data['id'],
            "sid" : data['id'],
            'uri': data['uri'],
         }
      )
      db_tracks.append(record)
      # print(len(db_tracks))
      db_tracks_sids.append(record.sid)
      db_tracks_map[record.sid] = record
   except pocketbase.utils.ClientResponseError:
      # TODO Already Exists...hmm not updating playlist?
      #TODO log
      # print('insert_track...ClientResponseError', data['name'], data['uri'])
      # sleep(3)
      # return
      #! 
      record = db_tracks_map[data['id']]#pb.collection(table).get_list(1, 1, {'spotify_id': data['id']}).items[0]
      # print(record.id)
   if genre:
      record.genres.append(genre)
      genres = list(set(record.genres))
      genres.sort()
      pb.collection(table).update(
      record.id,
         {
            "genres": genres
         }
      )
   
   return record

def scanMixes(): # artists table for queueing tracks

   system('clear')
   print('\nscanMixes')

   followed_mixes = [p for p in getFollowedPlaylists() if ' Mix' in p['name'][4:] and 'Radio' not in p['name']]
   if len(followed_mixes): #! if not in pb
      for p in followed_mixes: #! always check first; if len
         print('Unfollowing ', p['name'])
         sp.current_user_unfollow_playlist(p['id'])
      input('Update Mix Excludes List.')
      
      return #! - pb variable; mixes invalidation

   EXCLUDE = [
      'Early 2000s Indie Rock Mix',
      'Workout Indie Rock Mix',
      'Running Indie Rock Mix',
      'Remix Indie Pop Mix',
      'Italian Indie Pop Mix',
      # 'Monday Mix', #!
      # 'Tuesday Mix',
      # 'Wednesday Mix',
      # 'Thursday Mix',
      # 'Friday Mix',
      # 'Saturday Mix',
      # 'Sunday Mix',
      # 'Daily Mix',
   ]
   # for t in pb.collection('tracks').get_full_list():
   #    pb.collection('tracks').delete(t.id)
   """!
   Unfollowing  Save Me - Extended Mix
Unfollowing  Dance/Electronic Mix
Unfollowing  Indie Mix
Unfollowing  Vapor Twitch Mix
   """
   addlst = [
      'Discover Weekly',
      'Release Radar',
   ]
   for p in [p for p in db_playlists if ' Mix' in p.name[4:] or p.name in addlst]: #! start with just accumulating all genres
      if 'Radio' in p.name or p.name in EXCLUDE or p.name[0].isdigit():
         print('Skipping ', p.name)
         continue
      #newInsertPlaylist(); #specificity
      # get tracks
      # insert track - patch later - reduce calls
      if p.name in [
         'Remix Indie Pop Mix',
         'Monday Mix', #!
         'Tuesday Mix',
         'Wednesday Mix',
         'Thursday Mix',
         'Friday Mix',
         'Saturday Mix',
         'Sunday Mix',
         'Weekday Mix',
         'Daily Mix',
         'Daily Mix 1',
         'Daily Mix 2',
         'Daily Mix 3',
         'Daily Mix 4',
         'Daily Mix 6',
         'Daily Mix 5',
         'Discover Weekly',
         'Release Radar',
      ]:
         genre = None
      else:
         genre = p.name.split(' Mix')[0]
      print(p.name)
      for t in getTracks(p.sid): #! assume record..except
         insertTrackEntry(t, genre) #sync update specificity
   
   return #! patch uri for tracks

# radios
# genre mixes
def buildCollections(): #update to higher specificity; if removed from general, remove

   return 

# new ~ true && release_date > "2022-12-32"
# new ~ True && genres_str ~ "%Spanish Indie Pop%"
def queueNewTracks(limit=50, genre=None):

   return

TAGS = [
   '#tag-playlist',
   '#tag-memory',
   '#tag-year',
   '#tag-genre',
   '#tag-collection',
   '#tag-artistcollection',
]
#! update locally - invalidate on update
personal = [p for p in playlists() if '#tag-playlist' in p['name']]
memory = [p for p in playlists() if '#tag-memory' in p['name']]
mixes = [p for p in playlists() if ' Mix' in p['name'][4:]]
radios = [p for p in playlists() if ' Radio' in p['name'][6:]]

local_db = {}
now = datetime.now()
db_tracks = pb.collection('tracks').get_full_list()
db_tracks_sids = [t.sid for t in db_tracks]
db_tracks_map = {}
for record in db_tracks:
   db_tracks_map[record.sid] = record
   pb.collection('tracks').update(
      record.id,
      {
         'genres_str': ','.join(record.genres),
      }
   )
def updateTracksTableWithHeard(): #! artists table

   # for p in [p for p in playlists() if p['owner']['id'] == usr]:
   #    for t in getTracks(p['id']):
   #       print(t['track']['name'], t['track']['id'])
   #       try:
   #          record = db_tracks_map[t['track']['id']] #pb.collection('tracks').get_list(1, 50, {"sid": t['track']['id']})
   #       except:
   #          record = insertTrackEntry(t)
   #       # print(len(record.items))
   #       pb.collection('tracks').update(
   #          record.id,
   #          {
   #             'new': False,
   #          }
   #       )

   for a in db_artists:
      print(a.name)
      for t in a.queue:
         insertTrackEntry(t)
      for t in a.heard:
         insertTrackEntry(t)
         pb.collection('tracks').update(
            db_tracks_map[t].id,
            {
               'new': False,
            }
         )
      sleep(1)


def queueSomething(genre=None):
   print('\nqueueSomething')
   tmp = pb.collection('tracks').get_full_list()
   tmp = [t for t in tmp if t.new == True]
   if genre:
      tmp = [t for t in tmp if genre in t.genres]
   tmp.sort(key=lambda x: x.release_date, reverse=True)
   for record in tmp[:50]:
      sp.add_to_queue(record.sid)
      pb.collection('tracks').update(
         record.id,
         {
            'new': False,
         }
      )

if __name__ == '__main__':
   print('Start')
   #! artist popularity changes
   if False:
      # updateTracksTableWithHeard()
      queueSomething()


      pass
   else:

      # move all saved to cycle

      # newSyncPlaylistsToDB() # syncPlaylistsToDB()
      
      # for all mixes, scan into lookup table
      scanMixes()
      queueSomething()

      # move all saved to genre

      # on repeat to year

      # remove years from saved
      
      # remove all personal playlists from saved, year, genre, general playlists

      # queue tracks




   pass
   