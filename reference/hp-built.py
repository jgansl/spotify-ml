import pocketbase
import pandas as pd
import requests

# take a track from spotipy and insert it into a pandas dataframe
def insert_track(track):
  track_id      = track['track']['id']
  track_name    = track['track']['name']
  artist        = track['track']['artists'][0]['name']
  album         = track['track']['album']['name']
  release_date  = track['track']['album']['release_date']
  duration      = track['track']['duration_ms']
  popularity    = track['track']['popularity']
  explicit      = track['track']['explicit']
  track_df      = pd.DataFrame({
    'track_id':     [track_id],
    'track_name':   [track_name],
    'artist':       [artist],
    'album':        [album],
    'release_date': [release_date],
    'duration':     [duration],
    'popularity':   [popularity],
    'explicit':     [explicit]
  })
  return track_df



def insert_dataframe_to_pocketbase(df, table_name, pb_url):
  """
  Insert a pandas DataFrame into a PocketBase table.
  
  :param df: pandas DataFrame to insert
  :param table_name: name of the PocketBase table
  :param pb_url: base URL of your PocketBase instance
  """
  # Convert DataFrame to list of dictionaries
  records = df.to_dict('records')
  
  # Endpoint for creating records
  endpoint = f"{pb_url}/api/collections/{table_name}/records"
  
  # Insert each record
  for record in records:
    try:
      response = requests.post(endpoint, json=record)
      response.raise_for_status()
      print(f"Inserted record: {response.json()['id']}")
    except requests.exceptions.RequestException as e:
      print(f"Error inserting record: {e}")

# Example usage:
# df = pd.DataFrame(...)  # Your DataFrame
# pb_url = "http://127.0.0.1:8090"  # Your PocketBase URL
# insert_dataframe_to_pocketbase(df, "your_table_name", pb_url)

# insert dataframe into pocketbase table


