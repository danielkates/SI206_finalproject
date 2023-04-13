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
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

client_id = '26030839b43a4f679198b03e28a7ba1a'
client_secret = 'e69ba868f41e4029a74096a9d997abae'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_top_100_songs():
    # Retrieve top 100 songs from Spotify API
    top_tracks = sp.current_user_top_tracks(limit=100, time_range='year')
    
    # Store data in SQLite database
    conn = sqlite3.connect('music_data.db')
    c = conn.cursor()
    
    for track in top_tracks['items']:
        title = track['name']
        artist = track['artists'][0]['name']
        genre = track['genres'][0]
        listeners = track['popularity']
        
        c.execute('''CREATE TABLE IF NOT EXISTS spotify_top_100
                (id INTEGER PRIMARY KEY,
                 title TEXT,
                 artist TEXT,
                 genre TEXT,
                 listeners INTEGER)''')
        
    conn.commit()
    conn.close()

def get_genre_breakdown():
    # Calculate breakdown of total listeners per genre
    conn = sqlite3.connect('music_data.db')
    c = conn.cursor()
    
    c.execute("SELECT genre, SUM(listeners) FROM spotify_top_100 GROUP BY genre")
    data = c.fetchall()
    
    # Calculate percentage of songs in top 100 for each genre
    c.execute("SELECT COUNT(*) FROM spotify_top_100")
    total_songs = c.fetchone()[0]
    
    for row in data:
        genre = row[0]
        total_listeners = row[1]
        num_songs = c.execute("SELECT COUNT(*) FROM spotify_top_100 WHERE genre=?", (genre,)).fetchone()[0]
        percentage = round(num_songs / total_songs * 100, 2)
        print(f"{genre}: {percentage}% ({num_songs} songs) - {total_listeners} listeners")
    
    conn.close()


def main():
    # Define database file
    db_file = "spotify_top100.db"

    # Check if database file exists
    if not os.path.exists(db_file):
        # If not, create a new database file and populate it with top tracks
        conn = sqlite3.connect(db_file)
        get_top_100_songs()
    else:
        # If it exists, analyze the data in the database
        get_genre_breakdown()


if __name__ == '__main__':
    main()

