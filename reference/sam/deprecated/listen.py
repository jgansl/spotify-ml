# import re
"""
- move saved to library
- remove two week old, remove frm library if in genre
- tagging system so script does not have to be manually updated
- genre new
- k clustering new sorting and library sorting
- cross api refrenecing 
- ytm sycning
- new sorting by artists - new, spotify genre, and training - auto update playlists labeled #artists
- check artists for new tracks ... personal release radar
"""
from os import system
from time import sleep
from pydash import flatten
import re

from functions import SAM, sp, jprint, mem, TRACK, SAVED

# import streamlit as st
# from streamlit_autorefresh import st_autorefresh

# import pocketbase
from pocketbase import PocketBase
# from pocketbase.client import ClientResponseError


def next_track(*args):
   sp.next_track(device_id)

def manual_next():
   sp.next_track(device_id)
   sleep(1)

# try:
pb = PocketBase('http://127.0.0.1:8092', 'en-US')
# except pocketbase.client.ClientResponseError:
#    print('db not found')
#    exit()
# if 'db' not in st.session_state:
#    print('init db')
#    st.session_state.
db = {}
for i in pb.records.get_full_list('spotify'):
   #st.session_state.
   db[i.sid] = i

# if 'device_id' not in st.session_state:
devices = [d for d in sp.devices()['devices'] if d['is_active']]
if len(devices):
      # st.session_state.
   device_id = devices[0]['id']
      # st.session_state.refresh_device_id = False
   # print('init device_id', devices[0]['name'])

last = None
# if 'last' not in st.session_state:
#    print('init last')
#    st.session_state.last = None

# refresher = st_autorefresh(interval=3000, limit=100, key="listen") 

# SETTINGS
# #config
skip_saved = False # does not save; for daily mixes
skip_heard = False #daily mixes
skip_old = False #none 2020s
daily_new_artists_only = False #queue top tracks; explore
queue_top_tracks = False #reocrd and hide
scan_in = 0
seek_around = True
# remove old entries - skip, last updated?


p_new = mem.pname('New', create=True)
queue_unheard = False #datecheck - pb variables
# unheard_name = 'Daily Mix 2'
if queue_unheard:
   for z in [ #pb implicitly follow
      'Release Radar',
      'Discover Weekly',
      'Daily Mix 1',
      'Daily Mix 2',
      'Daily Mix 3',
      'Daily Mix 4',
      'Daily Mix 5',
      'Daily Mix 6',
      'Monday Mix',
      'Tuesday Mix',
      'Wednesday Mix',
      'Thursday Mix',
      'Friday Mix',
      'Saturday Mix',
      'Sunday Mix',
      'Pixel Garden'
   ]:
      tmplist = mem.diff(mem.diff(mem.get_track_ids(mem.pname(z)), [*db]), mem.get_track_ids(p_new))
      mem.move(None, p_new['id'], tmplist)
      for tmpid in tmplist:
         sp.add_to_queue(tmpid)
      #add to playlist and remove

if queue_unheard:
   for z in [ #pb implicitly follow
      'Folk & Acoustic Mix',
      'Hip Hop Mix',
      'House Mix',
      'Indie Mix',
      'Dance/Electronic Mix',
      'Drum and Bass Mix',
      'Wake Up Mix',
   ]:
      tmpp = mem.pname(re.sub('Mix', 'New', z))
      tmplist = mem.diff(mem.diff(mem.get_track_ids(mem.pname(z)), [*db]), mem.get_track_ids(tmpp))
      mem.move(None, tmpp['id'], tmplist)
      # for tmpid in tmplist:
      #    sp.add_to_queue(tmpid)
      #add to playlist and remove

   exit()

while True:
   # if len(queue):
   #    pass
   cur = sp.currently_playing()
   if cur: #settimouet to refresh
      cur_item = cur['item']
      if not cur_item:
         sleep(1)
         continue
      sec = (cur['item']['duration_ms'] - cur['progress_ms']) / 1000
      cur_sid = cur_item['id'] #if in [*db] skip


      # if st.session_state.
      if last != cur_sid:
         mem.move(p_new['id'], None, [cur_sid]) #! egnre new
      
         if device_id: #or
            if skip_saved and cur_sid in mem.sids: #skip; skip count?
               print('saved')
               manual_next()
               last = cur_sid
               continue
            
            #! if skip_old and cur_item['album']['release_date']: #skip; skip count?
            #    manual_next

            if skip_heard and cur_sid in [*db]:# and cur_sid not in mem.sids: #skip; skip count?
               print('heard')
               manual_next()
               last = cur_sid
               continue
            
            if cur_sid in [*db] and db[cur_sid].hide:
               print('hidden')
               manual_next()
               last = cur_sid
               continue

         system('clear')
         cur_artists = cur_item['artists']
         cur_artist_ids = [a['id'] for a in cur_item['artists']]
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

         # if cur_sid in [*st.session_state.db]: #record should have been updated
         if cur_sid in [*db]: #record should have been updated
            #st.session_state.
            db[cur_sid] = pb.records.update('spotify', db[cur_sid].id, {"sid":cur_sid, "playcount":db[cur_sid].playcount + 1, 'genres': genres, "saved": cur_sid in mem.sids})
         else:
            db[cur_sid] = pb.records.create('spotify', {"sid":cur_sid, "playcount":1, 'genres': genres, "saved": cur_sid in mem.sids})
      
         print(cur_item['name'])
         for g in genres:
            print(g)
         jprint(feats)
         last = cur_sid
      
   # if device_id and cur and seek_around:
   #    sp.seek_track(cur['progress_ms'] + 10000, device_id)
   sleep(5)

#unhear - sedd genre and tempo; artist exploration; pi - server interface; pull chagnes daily