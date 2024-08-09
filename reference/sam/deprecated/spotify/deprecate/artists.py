from base import *
import pydash as _

# if artists not in playlist, add to new artist -> daily artists
#
# for genre in artist, if genre playlist exists, add, else, new artist

ps = [
   # 'Reduce',
   'Cache 0',
   'Cache 1',
   'Cache 2',
   'Cache 3',
   'Cache 4',
]
aids = set()
if os.path.exists('artists.json'):
   with open('artists.json', 'r') as f:
      aids = set(json.load(f))
# for p in ps:
#    for t in mem.retrieve(TRACK, pid=mem.pname(p)['id']):
#       aids.update([a['id'] for a in t['track']['artists']])

# with open('artists.json', 'w') as f:
#    json.dump(list(aids), f)