from base import *
from pydash import flatten
from re import sub
from concurrent.futures import ThreadPoolExecutor


def load(fn):
   jprint('Loading...')
   if os.path.exists(fn):
      with open(fn, 'r') as f:
         return json.load(f)
   else: return False
def save(data, fn, i=2):
   # if os.path.exists(fn):
   with open(fn, 'w') as f:
      json.dump(data, f, indent=i)

def checkYear(p, tracks):
   def evalYear(t):
      global untracked_pid, twentyten
      if 'item' in [*t]:
         t = t['item']
      if 'track' in [*t]:
         t = t['track']

      tid = t['id']
      rd = t['album']['release_date']
      try:
         year = datetime.strptime(rd,'%Y-%m-%d')
         year = year.year
      except ValueError: 
         if(rd[:4].isdigit()):
            year = int(rd[:4]) 
         else:
            return


      
      # if year.year.is_digit():
      lst = [tid]
      if(year >= 2020):
         # print('2020s')
         mem.move(
            untracked_pid, 
            twentytwenty['id'], 
            mem.diff(
               lst, 
               #mem.get_track_ids(
               twentytwenty
               # )
            )
         )
         # if tid in mem.sids and year < 2022:
         #    mem.move(SAVED, None, lst)
      if(year >= 2010 and year < 2020):
         # print('2010s')
         try:
            mem.move(p['id'], twentyten['id'], lst)
            if tid in mem.sids:
               mem.move(SAVED, None, lst)
         except TypeError: 
            print(t['name'])
            pass
      if(year >= 2000 and year < 2010):
         # print('00s')
         mem.move(p['id'], twothousands['id'], lst)
         if tid in mem.sids:
            mem.move(SAVED, None, lst)
      if(year >= 1990 and year < 2000):
         # print('00s')
         mem.move(p['id'], ninties['id'], lst)
         if tid in mem.sids:
            mem.move(SAVED, None, lst)
      if(year >= 1980 and year < 1990):
         # print('80s')
         mem.move(p['id'], eighties['id'], lst)
         if tid in mem.sids:
            mem.move(SAVED, None, lst)
      if(year >= 1970 and year < 1980):
         # print('70s')
         mem.move(p['id'], eighties['id'], lst)
         if tid in mem.sids:
            mem.move(SAVED, None, lst)
   
   for t in tracks:
      # e.submit(evalYear, t)
      evalYear(t)
#
#
#
#
#
if __name__ == '__main__': #refactor
   e = ThreadPoolExecutor(max_workers=25)
   false = True
   devices = sp.devices()['devices']
   active_device = [d for d in devices if d['is_active']]
   controls = False
   if active_device:
      active_device = active_device[0]
      controls = True
      print('Active Device Found')

   # TODO auto dictionary generation
   nostalgia = mem.pname('Nostalgia')
   seventies = mem.pname('70s')
   eighties = mem.pname('80s')
   ninties = mem.pname('90s')
   twothousands = mem.pname('00s')
   twothousands_ids = mem.get_track_ids(twothousands)
   
   twentytwenty = mem.pname('20s')
   twentyten = mem.pname('2010s')
   twentyten_ids = mem.get_track_ids(twentyten)
   
   untracked = mem.pname('Untracked Cache')
   untracked_pid = untracked['id']
   untracked_ids = mem.get_track_ids(untracked)
   untracked_tracks = mem.retrieve(TRACK, pid=untracked_pid)
   
   #remove 2010s from saved #TODO do for each genre
   # mem.move(SAVED, None, twothousands_ids)
   # mem.move(SAVED, None, twentyten_ids)
   #! e.submit(checkYear, mem.saved)
   #SAVED checkYear(pobj, mem.retrieve(TRACK, pid=pobj['id'])[:50])
   for pstr in [
      # 'Dance/Electronic',
      # 'Drum and Bass',
      # 'Folk & Acoustic',
      # 'Hip Hop',
      # 'House',
      # 'Indie',
      # 'Pop',
      'Untracked Cache'
   ]:
      pobj = mem.pname(pstr, create=False)
      if not pobj:
         print(pstr,'not found')
      else:
         checkYear(pobj, mem.retrieve(TRACK, pid=pobj['id']))
         # e.submit(checkYear, pobj, mem.retrieve(TRACK, pid=pobj['id']))
         pass
   
   last = None
   # exit()
   while True:
      res = sp.currently_playing()

      if not res:
         print('Not Playing')
         sleep(3)
         continue

      t = res['item']
      sid = t['id']

      if last == sid:
         continue

      artists = sp.artists([a['id'] for a in t['artists']])['artists']
      genres = [a['genres'] for a in artists]

      checkYear(untracked, [t])
      
      os.system('clear')
      print(t['album']['release_date'])
      jprint(flatten(genres))
      for g in flatten(genres):
         if 'lo-fi' in g.lower():
            print(g)
            mem.move(untracked_pid, mem.pname('Lofi')['id'], [sid])
            if controls:
               sp.next_track(device['id'])
      print()
      print(','.join([a['name'] for a in artists]), '-', t['name'])

      last = sid
      sleep(2)
   pass