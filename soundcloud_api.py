from bs4 import BeautifulSoup
import requests
import re
import json
import sqlite3
import os
import numpy as np
import matplotlib.pyplot as plt
import soundcloud
import sqlite3

SOUNDCLOUD_CLIENT_ID = 'your_soundcloud_client_id'

def get_top_tracks():
    # Authenticate with SoundCloud API
    client = soundcloud.Client(client_id=SOUNDCLOUD_CLIENT_ID)

    # Retrieve top 100 tracks from SoundCloud API
    tracks = client.get('/tracks', limit=100, order='hotness')

    # Store top tracks in a SQLite database
    conn = sqlite3.connect('soundcloud_top_tracks.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS tracks (id TEXT PRIMARY KEY, name TEXT, artist TEXT, playback_count INTEGER, genre TEXT)')
    for track in tracks:
        track_id = str(track.id)
        name = track.title
        artist = track.user['username']
        playback_count = track.playback_count
        genre = '' # Set genre to empty string for now
        c.execute('INSERT OR REPLACE INTO tracks VALUES (?, ?, ?, ?, ?)', (track_id, name, artist, playback_count, genre))
    conn.commit()
    conn.close()

def get_genre_count(tracks):
    """
    Given a list of tracks, returns a dictionary with the total number of tracks per genre.
    """
    genre_count = {}
    for track in tracks:
        genre = track.genre
        if genre in genre_count:
            genre_count[genre] += 1
        else:
            genre_count[genre] = 1
    return genre_count

def get_genre_listeners(tracks):
    """
    Given a list of tracks, returns a dictionary with the total number of listeners per genre.
    """
    genre_listeners = {}
    for track in tracks:
        genre = track.genre
        listeners = track.playback_count
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
    c.execute("SELECT * FROM soundcloud_top100")
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
    print("SoundCloud Genre Counts:")
    print(genre_counts)
    print("SoundCloud Listener Counts:")
    print(listener_counts)

    # Close database connection
    conn.close()

    
def main():
    get_top_tracks()

if __name__ == '__main__':
    main()