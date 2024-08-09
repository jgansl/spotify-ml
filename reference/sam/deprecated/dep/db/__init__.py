#@see https://pypi.org/project/pocketbase/
from pocketbase.stores.base_auth_store import BaseAuthStore
from pocketbase import PocketBase#, BaseAuthStore # Client also works the same
# help(BaseAuthStore)
pb = PocketBase('http://127.0.0.1:8090', 'en-US') #base
# help(pb)
# help(pb.admins.auth_via_email)
# admin_data = pb.admins.auth_via_email("jgans6421@gmail.com", "Hab!scus1!")
# print(admin_data)
# print(pb.records.collection('users').listAuthMethods())

print(pb.records.get_one('spotify', '', {'sid':"4OoD2oTiQdH9rQ4pPnIAfT"}))
# print(pb.records.create('spotify', {"sid":"test2", "playcount":1}))
# print(pb.records.update('spotify', 'dlo78zt0oidp9eq', {"sid":"test2", "playcount":2}))

# print(type(pb.collections))
# help(pb.collections.get_list())
# print(pb.collections.get_list())
# print(type(pb.records))

# q