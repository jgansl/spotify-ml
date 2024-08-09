from mongoengine import *

connect('pi-spotify')

class Artist(Document):
   sid = StringField(required=True)
   
class Track(Document):
   sid = StringField(required=True)
   # genres = StringField(max_length=50)
   playcount = IntField()
   # attributes = StringField(max_length=50)
   hide = BooleanField()
   saved = BooleanField()