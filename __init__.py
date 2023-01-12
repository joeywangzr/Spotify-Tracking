import json
import os
import requests
import uuid
from credentials import id, secret
from flask import Flask, redirect, render_template, request

client_id = id
redirect_uri = 'http://localhost:8888/callback'

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/authorize', methods=["GET"])
def authorize():
    state = str(uuid.uuid4())

    return redirect('https://accounts.spotify.com/authorize?' + {
      "response_type": 'code',
      "client_id": client_id,
      "scope": "user-top-read",
      "redirect_uri": redirect_uri,
      "state": state
    });

if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)
    print(authorize())