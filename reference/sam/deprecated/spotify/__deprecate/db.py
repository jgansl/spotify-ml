#https://pypi.org/project/pocketbase/

from pocketbase import PocketBase # Client also works the same

client = PocketBase('http://127.0.0.1:8090')

...

# list and filter "example" collection records
result = client.records.get_list(
    "example", 1, 20, {"filter": 'status = true && created > "2022-08-01 10:00:00"'}
)

# authenticate as regular user
user_data = client.users.auth_via_email("test@example.com", "123456")

# or as admin
admin_data = client.admins.auth_via_email("test@example.com", "123456")