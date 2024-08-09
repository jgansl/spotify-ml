from os import system
from time import sleep
from pydash import flatten
import re

from functions import SAM, sp, jprint, mem, TRACK, SAVED

from concurrent.futures import ThreadPoolExecutor
ex = ThreadPoolExecutor(max_workers=25)

from pocketbase import PocketBase
from pocketbase.client import ClientResponseError
# try:
pb = PocketBase('http://127.0.0.1:8090', 'en-US') #else wirte to file to read next tiem -> pi
# except ClientResponseError:
#    exit

# s = SAM()

def listen():
   #config
   skip_heard = True #daily mixes



   #state
   last = None
   
   db = {}
   for i in pb.records.get_full_list('spotify'):
      db[i.sid] = i
   
   devices = [d for d in sp.devices()['devices'] if d['is_active']]
   if len(devices):
      device_id = devices[0]['id']
   
   while 1:
      cur = sp.currently_playing()
      
      if not cur:
         print('Not Playing') 
         sleep(3)
         continue


      cur_track = cur['item']
      cur_sid = cur_track['id']

      
      if cur_sid == last:
         sleep(3) #duration remaining
         continue

      # and not in liked songs
      if skip_heard and device_id and cur_sid in [*db] and cur_sid not in mem.sids: #skip; skip count?
         sp.next_track(device_id)
      
      if device_id and cur_sid in [*db] and db[cur_sid].hide:
         sp.next_track(device_id)

      # record = pb.records.get_full_list('spotify')[0]
      system('clear')

      #skip these requests if record - save bandwidth
      # insert artists
      cur_artists = cur_track['artists']
      cur_artist_ids = [a['id'] for a in cur_track['artists']]
      genres = flatten([a['genres'] for a in sp.artists(cur_artist_ids)['artists']])
      feats = sp.audio_features(cur_sid)[0]

      for key in [
         'key',
         'mode',
         'uri',
         'type',
         'id',
         'track_href',
         'analysis_url',
         'time_signature'
      ]:
         del feats[key]


      if cur_sid in [*db]: #record should have been updated
         db[cur_sid] = pb.records.update('spotify', db[cur_sid].id, {"sid":cur_sid, "playcount":db[cur_sid].playcount + 1, 'genres': genres})
      else:
         db[cur_sid] = pb.records.create('spotify', {"sid":cur_sid, "playcount":1, 'genres': genres})

      print(cur_sid[:5], ','.join([a['name'] for a in cur_track['artists']]), '-', cur_track['name'])
      print(cur_track['album']['release_date'])
      print(', '.join(genres))
      jprint(feats)
      #attributes

      last = cur_sid
      sleep(3)

GENRE_MIXES = [
   'Dance/Electronic',
   'Drum and Bass',
   'Experimental Bass',
   'Folk & Acoustic',
   'Hip Hop',
   'House',
   'Indie',
   'Indie Electropop',
   'Pop',
   'Pop EDM',
   'R&B',
   # 'Vapor Soul',
   # 'Vapor Twitch'
]
def daily(): #reorder by release date
   for i in GENRE_MIXES:
      #find mix, collection
      mix = mem.pname(f'{i} Mix')
      col = mem.pname(f'{i} Collection')
      #add to collection
      lst = mem.diff(mem.get_track_ids(mix), mem.get_track_ids(col))
      print(i, len(lst))
      if len(lst):
         mem.move(None, col['id'], lst)



def integrate():
   for i in GENRE_MIXES:
      print(i)
      col = mem.pname(f'{i} Collection')
      ls = mem.pname('Library', create=False)
      mem.move(ls['id'], None, mem.intersect(mem.get_track_ids(col), mem.get_track_ids(ls))) #check
      col_saved = mem.pname(f'{i}')
      col_saved_lst = mem.diff(mem.get_track_ids(col_saved), mem.intersect(mem.get_track_ids(col), mem.sids)) #not working
      mem.move(None, col_saved['id'], col_saved_lst)
      print(len(col_saved_lst))
      col_tracks = mem.retrieve(TRACK, pid=col['id'])
      len_before = len(col_tracks)
      print('len_before:', len_before)
      col_tracks = sorted(col_tracks, key=lambda x: (x['track']['album']['release_date']), reverse=True)
      # jprint([[t['track']['album']['release_date'], t['track']['name']] for t in col_tracks])
      # for t in col_tracks:
      #    print(t['track']['album']['release_date'], t['track']['name'])
      lst = [t['track']['id'] for t in col_tracks]
      sp.playlist_replace_items(col['id'], []) 
      sleep(3)
      # mem.move(None, col['id'], lst)
      # count = 100
      # while count < len(lst):
      for t in lst:
         mem.move(None, col['id'], [t])
      #    count+=100
      sleep(7)
      col_tracks = mem.retrieve(TRACK, pid=col['id'])
      tmp = [t['track']['id'] for t in col_tracks]
      for i in range(len(tmp)): #check post order
         if tmp[i] != lst[i]:
            print(lst[i], tmp[i])

      len_after = len(mem.get_track_ids(col))
      print('len_after:', len_after)
      assert len_after == len_before
   
   
   return


if __name__ == '__main__':
   """
   - sync liked songs with playlist for radio
   - remove 2 week old songs -> library
   - remove nostalic, genres from library
   - move lirbary to genre favorite
   - 
   """
   daily() # concurrent
   #weekly
   # integrate() #update config when done and skip
   # # ex.submit(

   # move collection into subset and remove from liked cache
   for i in GENRE_MIXES:
      col = mem.pname(f'{i} Collection')
      col_saved = mem.pname(f'{i}')
      ls = mem.pname('Library')
      tmp_lst = mem.intersect(mem.get_track_ids(col), mem.get_track_ids(ls))
      print(i, len(tmp_lst))
      mem.move(ls['id'], col_saved['id'], tmp_lst) #check
      

   #remove from saved and liked songs
   #ytm
   #daily mix unheard, artist explore insertion into pocketbase
   # scan in daily mix, artists
   # listen()

   #recommendations - liked songs
   

   pass