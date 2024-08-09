
# completely controllable by spotify - remove artists from db
# DEF scan all saved and unowned playlists for new artists
# only artists in a personal playlist - new genre playlist
# TODO too many queries - keep tracks table ( keeps artists in query )- relational linking
# PATCH move all queue/heard into artists json fields; new playslists can be dissolved; artists can be updated
# sort artists by poplarity per genres -> daily genre artist; number of songs scanned, unheard
# seed rec - group artists
# channels liked songs
# remove cill house from house - cross genre
# queue new songs -> daily genre mix
# dailt mix -> genre via artists lookup? - population updating
# quantifying and training recommendation engine - playlist construction analysis - 11d map algorithms - mood training
# friend playlists#11 d artisting linking
# smart shuffling & analysis dash d3
# how to tra k new - > place in cache?
# sort by newest
# cross genres
#! 'Selected. Releases' generated an exception: 'genres'
#! testing account mirror

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

jprint = lambda x: print(json.dumps(x, indent=4))

import pocketbase
from pocketbase import PocketBase
from pocketbase.client import ClientResponseError
pb = PocketBase('http://127.0.0.1:8092', 'en-US')

def insert_artist(data):
   # jprint(data)
   # if 'genres' not in data or not data['genres']:
   #    data['genres'] = []
   # jprint(data)
   return pb.collection('artists').create(
      {
         "sid" : data['id'],
         "name": data['name'],
         "genres": data['genres'],
         "popularity": data['popularity'], #TODO changes?; 0-100
         "followers": data['followers']['total'], #TODO update
         "queue": [],
         "heard": []
      }
   )

def patch_artists():
   global db_artists, db_artists_ids
   db_heard = pb.collection('heard').get_full_list()
   # for track in db_heard[:1000]:
   def funct(track):
      # print('\t'+track.name) #TODO update names
      # if not artist.followers:
      # print(track.sid)
      aids = [a['id'] for a in sp.track(track.sid)['artists']]
      if aids and aids[0] not in db_artists_ids: #TODO find artist duplicates -  removoe both and rescan? iamalex -2
         data = sp.artists([aids[0]])['artists'][0]
         jprint(data['name'])
         # input()
         # try:
         #    artist.name = data['name']
         # except TypeError:
         #    print('\t SKIP')
         #    continue
         # artist.genres = data['genres']
         # artist.popularity = data['popularity']
         # artist.followers = data['followers']['total']
         # artist.queue = [] #get all tracks and remove one by one
         # artist.heard = []
         # jprint(artist.name)
         # pb.collection('artists').update(
            # artist.id,
         #    (dict)artist
         try: 
            art = insert_artist(data)
            db_artists_map[art.sid] = art
            db_artists_ids.append(data['id'])
            #TODO update heard
         except pocketbase.utils.ClientResponseError:
            print('\t SKIP ' + data['name'])
            return # continue
         # input()
      else:
         art = db_artists_map[aids[0]]
      
      if not art.heard:
         art.heard = []
      art.heard.append(track.sid)
      try: # TODO patch IDS
         pb.collection('artists').update(
            art.id,
            {
               'heard': list(set(art.heard))
            }
         )
         #! watch popularity flucuations
         #! find duplicate artists
         # res = pb.collection('queue').get_list(1, 2, {'filter': 'sid = "' + track.sid+'"'})
         # print(res.items)
         # if len(res.items) > 1:
         #    print('ERROR: '+track.sid)
         #    input('Continue?')
         # res = res.items[0]
         # print(res.sid == track.sid)
         # print(res.id == track.id)
         pb.collection('heard').delete(
            track.id
         )
      except pocketbase.utils.ClientResponseError:
         print('\t SKIP: ' + track.sid)
      # input('Continue?')
      sleep(0.2)
   
   with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
      # Start the load operations and mark each future with its URL
      future_to_url = {executor.submit(funct, track): track for track in db_heard[:1000]}
      for future in concurrent.futures.as_completed(future_to_url):
         url = future_to_url[future]
         try:
            data = future.result()
         except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
   
   return

def liked_remixed():

   return

def scan_in_artists(): #TODO collect all collection, cache, new
   global db_artists, db_artists_ids, removable_sids

   # TODO channels
   playlist_list = [ # remove deep house focus from house, sync progressive house with focus deep house- remove from liked?
      'Release Radar',
      'Discover Weekly',
      # 'On Repeat',

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

      # 'Anti Anxiety Mix'
      'Aussietronica Mix',
      'Collaboration Mix',

      # '2010s Mix',
      'Bass Arcade',
      # 'Deep House 2023',
      'Folk Pop',
      'Fresh Finds Folk',
      'Fresh Finds Dance',
      'Selected. Releases',
   ]


   def func(p):
      print(p)

      # TODO saved (patch)
      # for all saved, unowned
      # for p in playlist_list:
      p = sam.pname(p)
      tracks = sam.retrieve(TRACK, pid=p['id'])
      queue_ids = [rec.sid for rec in pb.collection('queue').get_full_list()]
      for t in tracks:
         primary_artist = sp.artists([t['track']['artists'][0]['id']])['artists'][0]
         # jprint(primary_artist) #! TODO
         primary_aid = primary_artist['id']
         if primary_aid not in db_artists_ids:
            print('\t'+primary_artist['name'])
            try:
               record = insert_artist(primary_artist)
            except pocketbase.utils.ClientResponseError:
               print('\tERR'+primary_artist['name']) #Chet porter
               """
               Daily Mix 1
                  Steve James
                  ERRSteve James
               """
               # input('Continue?')
            # db_artists_map[record.sid] = record
            db_artists_map[primary_aid] = record
            db_artists_ids.append(primary_aid)
         else:
            # pb.collection('artist').get(primary_aid)
            """non-reocurring
            record = db_artists_map[t['track']['artists'][0]['id']]
            KeyError: '1BjaGDkxwa2fb2pSCXlFXb'"""
            try:
               record = db_artists_map[primary_aid]
            # print(t['track']['artists'][0]['name'])
            # input(record.name)
            except KeyError:
               print('\tKEYERR'+primary_artist['name'])
         
         record.heard = record.heard or []
         que = record.queue or []
         #TODO remove new into artists unheard -> add artist to Artists - Cache?
         que.append(t['track']['id'])
         que = list(set(que).difference(set(record.heard)))
         record.queue = que

         if len(record.queue):
            try: #if que.length
               pb.collection('artists').update(record.id, 
                  {
                     # 'heard': record.heard,
                     'queue': que
                  }
               )
            except ClientResponseError:
               jprint(que)
               print(record.id)
               # input('Continue?')
         # else:
         #    continue

         #! 'Saturday Mix' generated an exception: expected string or bytes-like object, got 'dict'
         if (
            t['track']['id'] not in queue_ids and 
            t['track']['id'] not in record.heard and #[t.sid for t in record.heard] and 
            t['track']['id'] not in record.queue #[t.sid for t in record.que]
         ):
            pb.collection('queue').create({
               'sid': t['track']['id'],
               # 'genre_mix': genre, #! TODO
               'name': t['track']['name'],
               'artist': t['track']['artists'][0]['id'],
               'artist_genres': record.genres
            })
            queue_ids.append(t['track']['id'])
   # for p in playlist_list:
   #    func(p)
   # RACE CONDITION
   with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
      # Start the load operations and mark each future with its URL
      future_to_url = {executor.submit(func, p): p for p in playlist_list}
      for future in concurrent.futures.as_completed(future_to_url):
         url = future_to_url[future]
         try:
            data = future.result()
         except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
         # else:
         #    print('%r page is %d bytes' % (url, len(data)))

   return

def analyze_genre():
   print()
   genres_list = [ #TODO testing
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
   ]

   # for genre in genres_list:
   def funct(genre):
      global db_artists_ids, db_artists_map
      print(genre)

      mix = sam.pname(genre + ' Mix')
      mix_ids = sam.get_track_ids(mix)
      if not len(mix_ids): return#continue

      #TODO exclude from taste
      artists = sam.pname('Artists - '+genre, description='#genre-artists')
      
      collection = sam.pname(genre)
      collection_ids = sam.get_track_ids(collection)
      
      cache = sam.pname('Cache - '+genre, description='#genre-cache')
      cache_ids = sam.get_track_ids(cache)
      
      
      new = sam.pname('New - '+genre, description='#genre-new')
      new_ids = sam.get_track_ids(new)
      # print(new['name']+',', len(new_ids), '\n')

      #TODO heard - permanent removal - db tracked
      
      tracks = []#!!!!!!collection_ids
      tracks.extend(collection_ids)
      tracks.extend(cache_ids)

      # extract saved collections
      coll_sids = sam.intersect(mix_ids, sam.sids)#pcache_ids)
      new_to_coll = sam.diff(coll_sids, collection_ids)
      sam.move(None, collection['id'], new_to_coll)
      # collection_ids.extend(new_to_coll)
      tracks.extend(new_to_coll)

      # for i in [new, artists]:
      tracks.extend(new_ids) #! not in another genre playlist or saved
      tracks.extend(sam.sids)
      new_tracks = sam.diff(mix_ids, tracks)
      #TODO track artists instaed; patch new
      sam.move(None, new['id'], new_tracks)
      # new_ids.extend(new_tracks)
      # TODO isnert into artists
      # for t in sam.retrieve(TRACK, pid=new['id']):
      #    art = sp.artists([t['track']['artists'][0]['id']])['artists'][0]
      #    if( art['id'] not in db_artists_ids ):
      #       record = insert_artist(art)
      #       db_artists_ids.append(art['id'])
      #       db_artists_map[art['id']] = record
      #    else:
      #       record = db_artists_map[art['id']]
      #    record.queue.append(t['track']['id'])
      #    pb.collection('artists').update(record.id, 
      #       {
      #          'queue': list(set(record.queue))
      #       }
      #    )
      #    sam.move(new['id'], None, [t['track']['id']])
      #    pb.collection('queue').create({
      #       'sid': t['track']['id'],
      #       'genre_mix': genre,
      #       'name': t['track']['name'],
      #       'artist': t['track']['artists'][0]['id'],
      #       'artist_genres': art.genres
      #    })

      # heard = sam.pname('Heard - '+genre, description='#genre-heard')
      # sp.current_user_unfollow_playlist(heard['id'])
      heard = sam.pname('Remove', description='#remove')
      for t in sam.retrieve(TRACK, pid=heard['id']):
         art = sp.artists([t['track']['artists'][0]['id']])['artists'][0]
         if( art['id'] not in db_artists_ids ):
            record = insert_artist(art)
            db_artists_ids.append(art['id'])
            db_artists_map[art['id']] = record
         else:
            record = db_artists_map[art['id']]
         record.heard.append(t['track']['id'])
         if t['track']['id'] in record.queue:
            record.queue.remove(t['track']['id'])
         pb.collection('artists').update(record.id, 
            {
               'queue': list(set(record.queue)),
               'heard': list(set(record.heard))
            }
         )
         sam.move(heard['id'], None, [t['track']['id']])
         sam.move(new['id'], None, [t['track']['id']])
      

      genre_ids = []
      genre_ids.extend(collection_ids)#sam.retrieve(TRACK, pid=collection['id'])
      genre_ids.extend(cache_ids)
      # for t in genre_ids:
      #    sp.tracks
      print(
         len(genre_ids), 
         len(new_ids), 
         len(sam.intersect(genre_ids, new_ids)), 
         len(sam.intersect(genre_ids, removable_sids))
      )
      res = sam.intersect(genre_ids, new_ids)
      if len(res):
         sam.move(new['id'], None, sam.intersect(genre_ids, new_ids))
      #TODO 85 25; if len then move
      if len(removable_sids):
         #TODO removed all
         sam.move(SAVED, None, sam.intersect(genre_ids, removable_sids))
         sam.move(SAVED, None, sam.intersect(cache_ids, sam.sids)) # remove cache immediately #h7
      
      for t in sam.retrieve(TRACK, pid=collection['id']):
         # print('\t'+t['track']['name'])
         if t['track']['album']['release_date'] < '2023':
            if t['track']['id'] not in cache_ids:
               sam.move(collection['id'], cache['id'], [t['track']['id']])
               sam.move(SAVED, None, [t['track']['id']]) #h7
            else:
               sam.move(collection['id'], None, [t['track']['id']])

      print('COMPLETE: '+genre+'\n')
   # for genre in genres_list:
   #    funct( genre )
   with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
      # Start the load operations and mark each future with its URL
      future_to_genre = {executor.submit(funct, genre): genre for genre in genres_list}
      for future in concurrent.futures.as_completed(future_to_genre):
         genre = future_to_genre[future]
         try:
            data = future.result()
         except Exception as exc:
            print('%r generated an exception: %s' % (genre, exc))
   return

def artist_genre_search(q, sort="popularity", reverse=False):
   #recommendation seeds - refine with attributes
   # or fine track attribute genres API
   subgenres_map = {

   }
   
   
   
   return

def scan_in_relatd_artists():
   """new field"""
   return

def recommend(): # GOAL - contained in spotify: seed -> liked songs pool sorting; explore all artists

   return


def youtube_music():
   return

def daily_artist():
   """followers < 50000 && followers > 100"""
   """genre"""
   return

def patch_followers():
   # follower < 50000 && poplarity > 80
   return

def bundle1():
   # patch_artists()
   analyze_genre()
   scan_in_artists() #TODO exc.submit(patch_artists)
   """queue tracks by popularity - currently empty"""


def get_artist_albums(aid):

   # artist_albums(artist_id, album_type=None, country=None, limit=20, offset=0)
   try:
      return sp.artist_albums(
         aid
      )
   except:
      return []

def new_releases():
   """
   add to heard - add once
   """
   global db_artists_map, today

   print('Fetching Recently Released Albums..')

   new_release = sam.pname('New Releases-')
   new_release_ids = sam.get_track_ids(new_release)
   additional = []
   for sid in [a['id'] for a in sp.current_user_followed_artists(50)['artists']['items']]:#! [*db_artists_map]: #! followed artists; daily artist
      albums = get_artist_albums(sid)['items']
      for album in albums: #? latest first?
         date = album['release_date']
         try:
            tmp2 = datetime.strptime( date, '%Y-%m-%d')
         except:
            if(date[:4] == '2023'):
               input(date + ' ' + 'Continue?')
            continue
         days = (today - tmp2).days
         if( days <= 2):
            # print('\t'+db_artists_map[sid].name + ' - '+ album['name']+'\t'+album['uri'])
            track_ids = [t['id'] for t in sp.album_tracks(album['id'])['items']]
            res = sam.diff(track_ids, new_release_ids)
            #! randomize
            sam.move(None, new_release['id'], res)
            new_release_ids.extend(track_ids)
            additional.extend(track_ids)

   for t in sam.retrieve(TRACK, pid=new_release['id']):
      tmp2 = datetime.strptime( t['added_at'], '%Y-%m-%dT%H:%M:%SZ')
      tmp3 = today - tmp2
      if( tmp3.days > 14):
         sam.move(new_release['id'], None, [t['track']['id']])

   return

def explore_saved_artists():
   print('Fetching Recently Released Albums..')

   new_release = sam.pname('New Releases-')
   new_release_ids = sam.get_track_ids(new_release)
   for s in sam.saved:
      artists = [a['id'] for a in s['track']['artists']]
      for sid in artists:
         albums = get_artist_albums(sid)['items']
         for album in albums: #? latest first?
            date = album['release_date']
            try:
               tmp2 = datetime.strptime( date, '%Y-%m-%d')
            except:
               if(date[:4] == '2023'):
                  input(date + ' ' + 'Continue?')
               continue
            days = (today - tmp2).days
            if( days <= 2):
               # print('\t'+db_artists_map[sid].name + ' - '+ album['name']+'\t'+album['uri'])
               track_ids = [t['id'] for t in sp.album_tracks(album['id'])['items']]
               res = sam.diff(track_ids, new_release_ids)
               #! randomize
               sam.move(None, new_release['id'], res)
               new_release_ids.extend(track_ids)
               # additional.extend(track_ids)

   for t in sam.retrieve(TRACK, pid=new_release['id']):
      tmp2 = datetime.strptime( t['added_at'], '%Y-%m-%dT%H:%M:%SZ')
      tmp3 = today - tmp2
      if( tmp3.days > 14):
         sam.move(new_release['id'], None, [t['track']['id']])


OWNED = [p for p in sam.playlists if p['owner']['id'] == usr]
PUBLIC_PERSONAL = []

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
   if( tmp3.days > 14):
      removable_sids.append(s['track']['id'])
print('REMOVABLE: '+str(len(removable_sids)))

db_artists = pb.collection('artists').get_full_list()
db_artists_map = {}
for i in pb.collection('artists').get_full_list():
   db_artists_map[i.sid] = i
db_artists_ids = [a.sid for a in db_artists]
if __name__ == '__main__':
   exc = PoolExecutor(max_workers=12)
   
   # bundle1()

   new_releases()
   explore_saved_artists()
