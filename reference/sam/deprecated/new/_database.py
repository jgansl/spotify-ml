import pocketbase
from pocketbase import PocketBase
from pocketbase.client import ClientResponseError

pb = PocketBase('http://127.0.0.1:8092', 'en-US')

###
#
# DB
#
###
###
#
# PLAYLIST
#
###
def updatePlaylist(record_id, data):
   return pb.collection('playlists').update(record_id, data)

def insertPlaylist(p):
   #! if type(data) == str: #ID provided
   #    data = retrieve(PLAYLIST)
   # else:
   #    data = data['track'] #! added_at

   # try: 
   pb.collection('playlists').create(
      {
         "sid": p['id'],
         "spotify_id": p['id'],
         "name": p['name'],
         "description": p['description'],
         'owner': p['owner']['id'],
         'owner_name': p['owner']['display_name'],
         "follow": True,
         "uri": p['uri'],
      }
   )
   return

