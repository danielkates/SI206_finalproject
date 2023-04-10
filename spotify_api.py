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
import spotipy
import spotipy.util as util


SPOTIFY_USERNAME = 'your_spotify_username'
SPOTIFY_CLIENT_ID = 'your_spotify_client_id'
SPOTIFY_CLIENT_SECRET = 'your_spotify_client_secret'
SPOTIFY_REDIRECT_URI = 'http://localhost:8000/callback'

def get_top_tracks():
    # Authenticate with Spotify API
    token = util.prompt_for_user_token(SPOTIFY_USERNAME, 'user-top-read',
                                       client_id=SPOTIFY_CLIENT_ID,
                                       client_secret=SPOTIFY_CLIENT_SECRET,
                                       redirect_uri=SPOTIFY_REDIRECT_URI)

    if token:
        # Retrieve top 100 tracks from Spotify API
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_top_tracks(limit=100, time_range='medium_term')
        tracks = results['items']

        # Store top tracks in a SQLite database
        conn = sqlite3.connect('spotify_top_tracks.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS tracks (id TEXT PRIMARY KEY, name TEXT, artist TEXT, popularity INTEGER, genre TEXT)')
        for track in tracks:
            track_id = track['id']
            name = track['name']
            artist = track['artists'][0]['name']
            popularity = track['popularity']
            genre = '' # Set genre to empty string for now
            c.execute('INSERT OR REPLACE INTO tracks VALUES (?, ?, ?, ?, ?)', (track_id, name, artist, popularity, genre))
        conn.commit()
        conn.close()

def get_genre_count(songs):
    """
    Given a list of songs, returns a dictionary with the total number of songs per genre.
    """
    genre_count = {}
    for song in songs:
        genre = song["genre"]
        if genre in genre_count:
            genre_count[genre] += 1
        else:
            genre_count[genre] = 1
    return genre_count

def get_genre_listeners(songs):
    """
    Given a list of songs, returns a dictionary with the total number of listeners per genre.
    """
    genre_listeners = {}
    for song in songs:
        genre = song["genre"]
        listeners = song["listeners"]
        if genre in genre_listeners:
            genre_listeners[genre] += listeners
        else:
            genre_listeners[genre] = listeners
    return genre_listeners

def analyze_data(db_file):
    # Connect to database
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Query all songs from top 100
    c.execute("SELECT * FROM spotify_top100")
    songs = c.fetchall()

    # Initialize genre and listener count dictionaries
    genre_counts = {}
    listener_counts = {}

    # Iterate through each song and update genre and listener counts
    for song in songs:
        genre = song[2]
        listeners = song[3]
        if genre not in genre_counts:
            genre_counts[genre] = 1
            listener_counts[genre] = listeners
        else:
            genre_counts[genre] += 1
            listener_counts[genre] += listeners

    # Print out genre and listener counts
    print("Spotify Genre Counts:")
    print(genre_counts)
    print("Spotify Listener Counts:")
    print(listener_counts)

    # Close database connection
    conn.close()

def main():
    get_top_tracks()

if __name__ == '__main__':
    main()