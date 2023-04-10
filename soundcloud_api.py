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

def main():
    get_top_tracks()

if __name__ == '__main__':
    main()