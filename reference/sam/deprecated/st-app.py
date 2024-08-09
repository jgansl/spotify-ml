"""
- safeguard for too many external operations
- cache
- currently cannot record when using spotify itself - no internal integrity checks
- stick utton in browser tab -like muting pause
- cycle lsradio and saved songs reload radio
"""

import re, os

from os import system
from time import sleep
from pydash import flatten

from functions import SAM, sp, jprint, mem, TRACK, SAVED
from concurrent.futures import ThreadPoolExecutor
exe = ThreadPoolExecutor(max_workers=25)

import streamlit as st
from streamlit_autorefresh import st_autorefresh
# count = st_autorefresh(interval=3000, limit=100, key="listen") #must prevent skipping in certain manners in order to use spotify directly

from pocketbase import PocketBase
from pocketbase.client import ClientResponseError
# try:
pb = PocketBase('http://127.0.0.1:8090', 'en-US')
# except ClientResponseError: #does not work
#    exit()
if 'db' not in st.session_state:
   # st.write('init db')
   st.session_state.db = {}
   for i in pb.records.get_full_list('spotify'):
      st.session_state.db[i.sid] = i

# or st.session_state.refresh_device_id:
# del st.session_state.refresh_device_id
if 'device_id' not in st.session_state:
   devices = [d for d in sp.devices()['devices'] if d['is_active']]
   if len(devices):
      st.session_state.device_id = devices[0]['id']
      st.session_state.refresh_device_id = False
   # st.write('init device_id')

if 'avail_genres' not in st.session_state:
   st.session_state.avail_genres = sp.recommendation_genre_seeds()

if 'last' not in st.session_state:
   st.session_state.last = None
   st.session_state.last_name = None

cur = sp.currently_playing()

# c11, c12 = st.columns((2, 1))
def refresh_page():#msg, *args):
   global sec#, r 
   sleep(10)
   # sleep(sec + 1)
   st.experimental_rerun()
#r = 
# exe.submit(refresh_page)  # cancel
toggleSaved = False
def toggle_save_track(*args): #toggle #update mem.sids #! update visually
   if toggleSaved:
      return
   if cur_sid in mem.sids:
      #st.session_state.db[cur_sid] = 
      pb.records.update('spotify', st.session_state.db[cur_sid].id, {'saved': True})
      sp.current_user_saved_tracks_add([cur_sid])
   else:
      sp.current_user_saved_tracks_remove([cur_sid])
      pb.records.update('spotify', st.session_state.db[cur_sid].id, {'saved': False})
   toggleSaved = True
def hide_track(*args):
   # exe.submit(refresh_page, *args)
   # 2022-12-21 11:54:12.709 Thread 'ThreadPoolExecutor-5_0': missing ScriptRunContext
   # sleep(3)
   # st.write('hiding')#, args))
   st.session_state.db[cur_sid] = pb.records.update('spotify', st.session_state.db[cur_sid].id, {'hide': True})
   if st.session_state.device_id:
      sp.next_track(st.session_state.device_id)
def next_track(*args):
   sp.next_track(st.session_state.device_id)
def prev_track(*args):
   sp.previous_track(st.session_state.device_id)

#config
skip_saved = True # does not save; for daily mixes
skip_heard = True #daily mixes
skip_old = False #none 2020s
daily_new_artists_only = False #queue top tracks; explore
queue_top_tracks = False #reocrd and hide
scan_in = 0
# remove old entries - skip, last updated?
os.system('clear')
def manual_next():
   sp.next_track(st.session_state.device_id)
   sleep(1)
   st.experimental_rerun()
if cur: #settimouet to refresh
   sec = (cur['item']['duration_ms'] - cur['progress_ms']) / 1000
   cur_item = cur['item']
   cur_sid = cur_item['id'] #if in [*db] skip

   if st.session_state.device_id: #or
      if skip_saved and cur_sid in mem.sids: #skip; skip count?
         manual_next()
      
      #! if skip_old and cur_item['album']['release_date']: #skip; skip count?
      #    manual_next

      if skip_heard and cur_sid in [*st.session_state.db] and cur_sid not in mem.sids: #skip; skip count?
         manual_next()
      
      if cur_sid in [*st.session_state.db] and st.session_state.db[cur_sid].hide:
         manual_next()
   
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
   
   if cur_sid in [*st.session_state.db]: #record should have been updated
      st.session_state.db[cur_sid] = pb.records.update('spotify', st.session_state.db[cur_sid].id, {"sid":cur_sid, "playcount":st.session_state.db[cur_sid].playcount + 1, 'genres': genres, "saved": cur_sid in mem.sids})
   else:
      st.session_state.db[cur_sid] = pb.records.create('spotify', {"sid":cur_sid, "playcount":1, 'genres': genres, "saved": cur_sid in mem.sids})
   

   st.write(cur_item['name'], sec, 'Seconds')
   st.write(f'Previously: {st.session_state.last_name}')
   if st.session_state.last != cur_sid:
      st.session_state.last = cur_sid
      st.session_state.last_name = cur_item['name']
   c21, c23, c24, c22 = st.columns(4)#(1, 1, 1))
   #not workign - skips track 
   if cur_sid in mem.sids:
      c24.button('Save', on_click=toggle_save_track) #state change highlight
   else:
      c24.button('unSave', on_click=toggle_save_track) #state change highlight
   c23.button('Hide', on_click=hide_track, args=[st.session_state.device_id])
   if st.session_state.device_id:
      c21.button('Prev', on_click=prev_track, args=[st.session_state.device_id])
      c22.button('Next', on_click=next_track, args=[st.session_state.device_id])
   
   print(cur_item['album']['release_date'])
   st.write(cur_item['album']['release_date'])
   st.write(', '.join(genres))
   st.write(feats)
   st.write(st.session_state.avail_genres)

   if st.session_state.device_id and scan_in:
      sleep(scan_in)
      sp.next_track(st.session_state.device_id)
      st.experimental_rerun()

# def my_widget(key):
#     st.subheader('Hello there!')
#     return st.button("Click me " + key)

# # This works in the main area
# clicked = my_widget("first")

# # And within an expander
# my_expander = st.expander("Expand", expanded=True)
# with my_expander:
#     clicked = my_widget("second")

# # AND in st.sidebar!
# with st.sidebar:
#     clicked = my_widget("third")

# #https://calmcode.io/streamlit/sidebar.html
# #https://pypi.org/project/streamlit-sidemenu/
# styles = """
# body {
#   margin: 0;
# }
# """