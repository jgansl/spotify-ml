from os import system
from time import sleep
import json

from sam import sam, sp, usr

jprint = lambda x: print(json.dumps(x, indent=4))


from pocketbase import PocketBase
from pocketbase.client import ClientResponseError
pb = PocketBase('http://127.0.0.1:8092', 'en-US')
COLL_Artists = pb.collection('artists').get_full_list() #TODO scan and insert
artist_sids = [record.sid for record in COLL_Artists]
COLL_Heard   = pb.collection('heard').get_full_list()
heard_sids = [record.sid for record in COLL_Heard] #liked sids?, update heard - track name
COLL_Queue   = pb.collection('queue').get_full_list()
queue_sids = [record.sid for record in COLL_Queue] # update release date
# TODO train hidden - overheard vs dislike
# move liked into cached - functionlize
# new table with queue field - artists


def requeue():
   print('Requeuing')
   for i in COLL_Heard:
      if str(i.created).split(" ")[0] == '2023-07-28': #TODO
         sp.add_to_queue(i.sid)
   

""" RESERVED
- p, t, s, sid, sids, tid, tids, track, tracks, track_ids
"""

# Settings
LISTEN        = False
QUEUE_UNHEARD = True
QUEUE_DELETE  = True
SEEK          = False
SKIP_HEARD    = False
# REQUEUE = True

# if REQUEUE:
#    requeue()
#    exit()

# Variables
OWNED = [p for p in sam.playlists if p['owner']['id'] == usr]
PUBLIC_PERSONAL = [ 
   #TODO make all playlists private unless in this list
]
MUSIC_TASTE = [
   #TODO make all playlists excluded unless in this list
]
for p in OWNED:
   if p['name'] not in PUBLIC_PERSONAL:
      sp.playlist_change_details(p['id'], public=False)

# UNOWNED = [p for p in sam.playlists if p['owner']['id'] != usr and 'Mix' in p['name']]
playlist_list = [ # remove deep house focus from house, sync progressive house with focus deep house- remove from liked?
   # 'Futurepop Mix',
   'Release Radar',
   'Discover Weekly',
   'Selected. Releases',
   'Discover Weekly',
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
   '2010s Mix',
   'Bass Arcade',
   # 'Deep House 2023',
   'Collaboration Mix',
   'Folk Pop',
   'Fresh Finds Folk',
   'Fresh Finds Dance',
   'Anti Anxiety Mix'
   'Aussietronica Mix'
]
UNOWNED = [p for p in sam.playlists if p['owner']['id'] != usr and p['name'] in playlist_list]
# UNOWNED.append(sam.pname('Release Radar'))
# UNOWNED.append(sam.pname('Discover Weekly'))
# UNOWNED.append(sam.pname('Selected. Releases'))
# UNOWNED.append(sam.pname('Deep House 2023'))


LAST = None



"""

"""
if QUEUE_UNHEARD:
   # scan in all personal
   total = len(OWNED)
   count = 0
   for p in OWNED:
      count = count + 1
      print(round(count * 100/total, 2))
      for tid in sam.get_track_ids(p):
         if tid not in heard_sids:
            # t = sp.track(tid)
            # for a in t['artists']:
            #    aid = a['id']
            #    print(a['name'])
            #    if aid not in artist_sids:
            #       obj = pb.records.create(
            #          'artists', 
            #          {
            #             "sid": aid,
            #             "name": a['name']
            #          }
            #       )
            #       COLL_Artists.append(obj)
            #       artist_sids.append(aid)
            obj = pb.collection('heard').create(
               {
                  "sid": tid,
                  # "name": t['name'],
                  # "artists": t['artists']
               }
            )
            COLL_Heard.append(obj)
            heard_sids.append(tid)
            # sleep(0.2)

   # scan through all spotify playlists
   total = len(UNOWNED)
   count = 0
   for p in UNOWNED:
      count = count + 1
      system('clear')
      print(round(count * 100/total, 2))
      print()
      for tid in sam.get_track_ids(p):
         if tid not in heard_sids and tid not in queue_sids: #TODO remove dev duplicates
            # t = sp.track(tid)
            # for a in t['artists']:
            #    aid = a['id']
            #    if aid not in artist_sids:
            #       obj = pb.records.create(
            #          'artists', #TODO check duplicates - rm both
            #          {
            #             "sid": aid,
            #             "name": a['name']
            #          }
            #       )
            #       COLL_Artists.append(obj)
            #       artist_sids.append(aid)
            # queue new - mark queue count
            if tid not in queue_sids:
               t = sp.track(tid)
               obj = pb.collection('queue').create( 
                  {
                     "sid": tid,
                     'name': t['name'],
                     # "artists": [a['id'] for a in t['artists']],
                     'release_date': t['album']['release_date'],
                     "queue_count": 1,
                     'date_added': '7/25'
                  }
               )
               COLL_Queue.append(obj)
               queue_sids.append(tid)
            # else: #TODO datetime check; does not occur because of queue_sids restriction
            #    # increment queue count in db
            #    item = [i for i in COLL_Queue if i.sid == tid][0]
            #    pb.records.update(
            #       'queue', 
            #       item.id,
            #       {
            #          "sid": item.sid,
            #          # 'name': t['name'],
            #          # "artists": [a['id'] for a in t['artists']],
            #          "queue_count": 1#item.queue_count + 1
            #       }
            #    )

            sleep(0.1)
   # exit()
   # sort by queue count (in-place)
   print('Queuing Up Tracks...')
   # clear queue
   COLL_Queue.sort(key = lambda obj: obj.release_date, reverse=True)
   # jprint( [obj.release_date for obj in COLL_Queue] )

   # queue - 200
   for r in COLL_Queue[:150]:
      sp.add_to_queue(r.sid)
      if QUEUE_DELETE:
         if r.sid not in heard_sids:
            t = sp.track(r.sid)
            obj = pb.collection('heard').create(
               {
                  "sid": r.sid,
                  'name': t['name'],
                  "artists": [a['id'] for a in t['artists']],
                  'date_added': '7/25'
               }
            )
            COLL_Heard.append(obj)
            heard_sids.append(r.sid)
         pb.collection('queue').delete(
            r.id 
         )
         COLL_Queue.remove(r)
         queue_sids.remove(r.sid)
      sleep(0.1)

   # scan in artists - queue tracks

   pass

if not LISTEN:
   exit()

COLL_Queue.sort(key = lambda obj: obj.release_date, reverse=True)

REDUCE = None#sam.pname('Reduce')
#move cache from saved
while 1:

   cur = sp.currently_playing() #TODO sp
   if not cur: #read error timoeut
      print('1')
      sleep(1)
      continue

   cur_track = cur["item"]
   cur_id    = cur_track["id"]

   if cur_id == LAST:
      sleep(3)
      continue

   LAST = cur_id
   # remove from reduce
   if REDUCE:
      sam.move(REDUCE['id'], None, cur_sid)
   if cur_id not in heard_sids:
      pb.collection('heard').create(
         {
            "sid": cur_id,
            'name': cur_track['name'],
            'release_date': cur_track['album']['release_date'],
            "artists": cur_track['artists'],
            'date_added': '7/25'
         }
      )
      heard_sids.append(cur_id)
      items = [i for i in COLL_Queue if i.sid == cur_id]
      if len(items):
         pb.collection('queue').delete(
            items[0].id 
         )
         queue_sids.remove(cur_id)

   system('clear')
   print(
      'Currently Playing:\n\n' + cur_track["name"] + ' by ' + ', '.join([a['name'] for a in cur_track["artists"]]) + ' ( ' + cur_track['album']['release_date'] + ' )'
   )

   
   sleep(5)
   # stop if last in queue if QUEUE
   pass