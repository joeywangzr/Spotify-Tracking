import base64
import json
import os
import requests
import uuid
import urllib.parse
from credentials import id, secret
from flask import Flask, redirect, render_template, request

client_id = id
client_secret = secret
redirect_uri = 'http://localhost:8888/callback'
state = str(uuid.uuid4())
access_token = None

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/login', methods=["GET"])
def login():

    params = {
      "response_type": 'code',
      "client_id": client_id,
      "scope": "user-top-read",
      "redirect_uri": redirect_uri,
      "state": state
    }

    url_safe_params = urllib.parse.urlencode(params)
    return redirect('https://accounts.spotify.com/authorize?' + url_safe_params)

@app.route('/callback')
def callback():

    # verify state
    compare_state = request.args.get('state')
    if state == compare_state or state != None:

        print("state verified")

        params = {
            "grant_type": "authorization_code",
            "code": request.args.get('code'),
            "redirect_uri": redirect_uri
        }

        headers = {
            "authorization": "Basic " + base64.b64encode(bytes(f"{client_id}:{client_secret}", "ISO-8859-1")).decode("ascii"),
            "content-type": "application/x-www-form-urlencoded"
        }

        r = requests.post('https://accounts.spotify.com/api/token', data=params, headers=headers)
        
        global access_token
        access_token = r.json()['access_token'] 

        get_top_songs(access_token, "short_term")

        return render_template('callback.html')

    else:
        # error
        return render_template('home.html')

@app.route('/refresh')
def refresh():
    
        params = {
            "grant_type": "refresh_token",
            "refresh_token": request.args.get('refresh_token')
        }
    
        headers = {
            "authorization": "Basic " + base64.b64encode(bytes(f"{client_id}:{client_secret}", "ISO-8859-1")).decode("ascii"),
            "content-type": "application/x-www-form-urlencoded"
        }

        r = requests.post('https://accounts.spotify.com/api/token', data=params, headers=headers)

        global access_token
        access_token = r.json()['access_token']

        return render_template('callback.html')

def get_top_songs(access_token, term_length):
    headers = {
        "Authorization": "Bearer " + access_token
    }

    params = {
        "time_range": term_length,
        "limit": 50
    }

    r = requests.get('https://api.spotify.com/v1/me/top/tracks', headers=headers, params=params)
    print(r.json())

if __name__ == '__main__':
    app.run(host="localhost", port=8888, debug=True)