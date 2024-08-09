# import re

import json
from os import system
from time import sleep
from pydash import flatten

from functions import SAM, sp, jprint, mem, TRACK, SAVED, usr

obj = {
    "liked": mem.sids,
}

# for p in mem.playlists:
#     try: 
#         obj[p['id']] = {
#             "name": p['name'],
#             "owner": p['owner']['id'],
#             "description": p['description'],
#             "track_ids": mem.get_track_ids(p)
#         }
#     except:
#         input(p['name'] + '. Continue?')
# print(type(obj))
# jprint(obj)
# with open('./restore_03_26_23.json', 'w') as f: #! auto-date
#     json.dump(obj,f,indent=2)

# exit()
lib = mem.pname('_library')
# print(lib)
for p in mem.playlists:
    if p['name'] == lib['name']:# or p['name'] == 'New':
        print("Library")
        continue
    if p['owner']['id'] == usr:
        trks = mem.get_track_ids(p)
        if(len(trks)):
            print(len(trks), p['name'])
            mem.move(None, lib['id'], trks)
        sp.current_user_unfollow_playlist(p['id'])
