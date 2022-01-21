import spotipy
import spotipy.util as util

from profileinfo import username, client_id, client_secret

token = util.prompt_for_user_token(
    username,
    scope=["user-read-recently-played", "playlist-modify-private"], # https://developer.spotify.com/documentation/general/guides/authorization/scopes/#playlist-modify-private
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri='http://localhost/'
)

sp = spotipy.Spotify(auth=token)
recently_played = sp.current_user_recently_played(limit=50)['items']
print(recently_played)
