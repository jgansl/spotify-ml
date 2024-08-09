from os import system
from time import sleep
from pydash import flatten
import re

from functions import SAM, sp, jprint, mem, TRACK, SAVED

from concurrent.futures import ThreadPoolExecutor
ex = ThreadPoolExecutor(max_workers=25)

from pocketbase import PocketBase
from pocketbase.client import ClientResponseError

from datetime import datetime
import unittest

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

def deDep():
   return

def removeOldSaved():
   added_max = 14
   format_data = "%Y-%m-%dT%H:%M:%SZ"
   now = datetime.now()

   lst = []
   for s in mem.saved:
      date = datetime.strptime(s['added_at'], format_data)
      diff = now - date
      if diff.days > added_max:
         lst.append(s['track']['id'])
   # print(round(len(lst) / len(mem.sids), 2))
   lib = mem.pname('Library')
   mem.move(None, lib['id'], mem.diff(lst, mem.get_track_ids(lib)))
   # mem.move(SAVED, None, lst)
   # mem.sids = sp.retrieve(SAVED)
   return

if __name__ == '__main__':
   '''
   prevent collection instead queue unheard, artists unheard, readio, 
   '''
   removeOldSaved()
   
   
   
   #  unittest.main()
   pass