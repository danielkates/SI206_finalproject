from bs4 import BeautifulSoup
import requests
import re
import json
import sqlite3
import os
import numpy as np
import matplotlib.pyplot as plt

def get_top_tracks():
    # Set up the API credentials
    CLIENT_ID = 'INSERT_CLIENT_ID_HERE'

    # Set up the API endpoint for retrieving the top tracks
    top_tracks_endpoint = 'https://api-v2.soundcloud.com/charts?kind=top&genre=soundcloud:genres:all-music&limit=100&offset=0&date=year'

    # Make a request to retrieve the top tracks
    response = requests.get(top_tracks_endpoint, headers={'client_id': CLIENT_ID})

    # Parse the track data from the response
    tracks_data = response.json()['collection']

    # Set up a connection to the SQLite database
    conn = sqlite3.connect('music_data.db')
    c = conn.cursor()

    # Insert the track data into the database
    for track in tracks_data:
        name = track['title']
        artist = track['user']['username']
        genre = track['genre']
        playback_count = track['playback_count']
        c.execute('INSERT INTO top_tracks (name, artist, genre, playback_count) VALUES (?, ?, ?, ?)',
                  (name, artist, genre, playback_count))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()