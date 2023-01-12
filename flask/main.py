import json
import os
import requests
import uuid
import urllib.parse
from credentials import id, secret
from flask import Flask, redirect, render_template, request

client_id = id
redirect_uri = 'http://localhost:8888/callback'

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/login', methods=["GET"])
def login():
    state = str(uuid.uuid4())

    params = {
      "response_type": 'code',
      "client_id": client_id,
      "scope": "user-top-read",
      "redirect_uri": redirect_uri,
      "state": state
    }

    url_safe_params = urllib.parse.urlencode(params)

    return redirect('https://accounts.spotify.com/authorize?' + url_safe_params)

if __name__ == '__main__':
    app.run(host="localhost", port=8888, debug=True)