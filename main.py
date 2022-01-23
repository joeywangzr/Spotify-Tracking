import spotipy
import spotipy.util as util
from pymongo import MongoClient
from profileinfo import username, client_id, client_secret, cluster
    
# database setup
client = MongoClient(cluster)
db = client.spotify
stats = db.stats

# spotify login
token = util.prompt_for_user_token(
    username,
    scope=["user-read-recently-played", "playlist-modify-private"], # https://developer.spotify.com/documentation/general/guides/authorization/scopes/#playlist-modify-private
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri='http://localhost/'
)

sp = spotipy.Spotify(auth=token)
recently_played = sp.current_user_recently_played(limit=50)['items']

most_recent = {'name':[],'artist':[],'duration':[],'played_at':[]}

for song in recently_played:
    my_dict = {'name':[],'artist':[],'duration':[],'played_at':[]}
    my_dict['name'] = (song['track']['name'])
    my_dict['artist'] = (song['track']['artists'][0]['name'])
    my_dict['duration'] = (song['track']['duration_ms'])
    my_dict['played_at'] = (song['played_at'])

    # check if updated
    if my_dict == most_recent:
        print('caught up!')
        break
    
    result = stats.insert_one(my_dict)
    print(f'Inserted: {my_dict}')

most_recent = {
    'name':recently_played[0]['track']['name'],
    'artist':recently_played[0]['track']['artists'][0]['name'],
    'duration':recently_played[0]['track']['duration_ms'],
    'played_at':recently_played[0]['played_at']
    }

print(f'most recent: {most_recent}')