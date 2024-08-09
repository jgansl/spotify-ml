from .sam import *
import json, os, re
from datetime import datetime, timedelta
# import pydash as _
from concurrent.futures import ThreadPoolExecutor
e = ThreadPoolExecutor(max_workers=5)
jprint = lambda x: print(json.dumps(x,indent=2))

# fn = 'data/lookup.json'
# if not(os.path.exists(fn)):
#    print('File Not Found')
#    exit()

# with open(fn, 'r') as f:
#    heard = json.load(f)

mem   = SAM(sp)
p_cache = mem.pname('Untracked Cache')
p_nost  = mem.pname('Nostalgia')
# p_red   = mem.pname('Reduce')

#! daily
#! CONST - prevent overwrite
radio_mixes = [p for p in mem.playlists if 'Mix' in p['name'] or 'Radio' in p['name']]
unowned     = [p for p in mem.playlists if p['owner']['id'] != usr]
owned     = [p for p in mem.playlists if p['owner']['id'] == usr]
colls       = [p for p in mem.playlists if '.collection' in p['description']]

spotify_genres = [
   'Blues',
   'Chill',
   'Dance/Electronic',
   'Drum and Bass',
   'Folk & Acoustic',
   'Hip Hop',
   # 'Happy',
   'House',
   'Indie',
   # 'Jazz',
   # 'Moody',
   # 'Soul',
   'Pop',
   'R&B',
]

pull_spotify_genres = [
   # 'Blues',
   'Chill',
   'Dance/Electronic',
   'Drum and Bass',
   'Folk & Acoustic',
   'Hip Hop',
   'House',
   'Indie',
   'Pop',
   # 'R&B',
]

years = [
   '2010s'
   '2000s'
   '90s'
   '80s'
   '70s'
]