from os import system
from time import sleep
from pydash import flatten
import re
from functions import SAM, sp, jprint, mem, TRACK, SAVED
from pocketbase import PocketBase
pb = PocketBase('http://127.0.0.1:8092', 'en-US')
db = {}
for i in pb.records.get_full_list('spotify'):
   db[i.sid] = i
devices = [d for d in sp.devices()['devices'] if d['is_active']]
while not len(devices):
   print('Not Playing')
   sleep(2)
   devices = [d for d in sp.devices()['devices'] if d['is_active']]
if len(devices):
   device_id = devices[0]['id']

# variables
last = None
p_new = mem.pname('New', create=True)

#helper functions
def next_track(*args):
   sp.next_track(device_id)

def manual_next():
   sp.next_track(device_id)
   sleep(1)

#! remoev db from genre new
#! scan library in
for s in mem.saved:
   sid = s['track']['id']
   if sid not in [*db]: #record should have been updated
      db[sid] = pb.records.create('spotify', {"sid":sid, "playcount":1 })#!, 'genres': genres, "saved": cur_sid in mem.sids})



####
#
# Settings
#
####
skip_heard  = True
seek_around = True
count = 0
while True:
   cur = sp.currently_playing()
   if cur:
      cur_item = cur['item']
      if not cur_item:
         print('no item')
         sleep(1)
         continue
      cur_sid = cur_item['id'] #if in [*db] skip
      sec = (cur['item']['duration_ms'] - cur['progress_ms']) / 1000

      if last != cur_sid:
         count = 0
         mem.move(p_new['id'], None, [cur_sid]) #! genre new
      
         if device_id:
         #    if skip_saved and cur_sid in mem.sids: #skip; skip count?
         #       print('saved')
         #       manual_next()
         #       last = cur_sid
         #       continue
            
         #    #! if skip_old and cur_item['album']['release_date']: #skip; skip count?
         #    #    manual_next

            if skip_heard and cur_sid in [*db]: # and cur_sid not in mem.sids: #skip; skip count?
               print('heard')
               manual_next()
               last = cur_sid
               continue
            
         #    if cur_sid in [*db] and db[cur_sid].hide:
         #       print('hidden')
         #       manual_next()
         #       last = cur_sid
         #       continue

         system('clear')
         cur_artists = cur_item['artists']
         #! check db rather than send request
         cur_artist_ids = [a['id'] for a in cur_item['artists']]
         genres = flatten([a['genres'] for a in sp.artists(cur_artist_ids)['artists']])
         
         feats = sp.audio_features(cur_sid)[0]
         if feats:
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
            db[cur_sid] = pb.records.update('spotify', db[cur_sid].id, {"sid":cur_sid, "playcount":db[cur_sid].playcount + 1, 'genres': genres, "saved": cur_sid in mem.sids})
         else:
            db[cur_sid] = pb.records.create('spotify', {"sid":cur_sid, "playcount":1, 'genres': genres, "saved": cur_sid in mem.sids})
      
         print(cur_item['name'])
         for g in genres:
            print(g)
         if feats:
            jprint(feats)
         last = cur_sid

   if device_id and cur and seek_around:
      if count > 3:
         manual_next()
      else:
         sp.seek_track(cur['progress_ms'] + 10000, device_id)
         count += 1
   sleep(5)