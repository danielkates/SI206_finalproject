import requests
from bs4 import BeautifulSoup
import sqlite3
import os
import json
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

def get_top_tracks():
    # Set up the API credentials
    CLIENT_ID = 'INSERT_CLIENT_ID_HERE'
    CLIENT_SECRET = 'INSERT_CLIENT_SECRET_HERE'

    # Set up the authentication headers
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }

    # Make a request to retrieve the access token
    auth_response = requests.post('https://accounts.spotify.com/api/token', {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    # Parse the access token from the response
    access_token = auth_response.json()['access_token']

    # Set up the API endpoint for retrieving the top tracks
    top_tracks_endpoint = 'https://api.spotify.com/v1/charts/top?limit=100&offset=0&country=global&type=tracks&time_range=year'

    # Make a request to retrieve the top tracks
    response = requests.get(top_tracks_endpoint, headers=headers)

    # Parse the track data from the response
    tracks_data = response.json()['tracks']

    # Set up a connection to the SQLite database
    conn = sqlite3.connect('music_data.db')
    c = conn.cursor()

    # Create a table to store the track data
    c.execute('''CREATE TABLE IF NOT EXISTS top_tracks
                 (id INTEGER PRIMARY KEY,
                  name TEXT,
                  artist TEXT,
                  genre TEXT,
                  popularity INTEGER)''')

    # Insert the track data into the database
    for track in tracks_data:
        track_id = track['id']
        track_endpoint = f'https://api.spotify.com/v1/tracks/{track_id}'
        track_response = requests.get(track_endpoint, headers=headers)
        track_data = track_response.json()
        name = track_data['name']
        artist = track_data['artists'][0]['name']
        genres = track_data['genres']
        popularity = track['popularity']
        for genre in genres:
            c.execute('INSERT INTO top_tracks (name, artist, genre, popularity) VALUES (?, ?, ?, ?)',
                      (name, artist, genre, popularity))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()