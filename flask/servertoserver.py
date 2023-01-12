import json
import requests
from credentials import id, secret

client_id = id
client_secret = secret

url = "https://accounts.spotify.com/api/token"
headers = {"Authorization": "Basic", "Content-Type": "application/x-www-form-urlencoded"}
data = {"grant_type": "client_credentials"}

initial_call = requests.post(url, headers=headers, data=data, auth=(client_id, client_secret)).json()

access_token = initial_call['access_token']

get_data = requests.get("https://api.spotify.com/v1/search?q=artist:abba&type=album", headers={"Authorization": "Bearer " + access_token}).json()

print(get_data)