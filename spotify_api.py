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

import sqlite3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = 'your_client_id_here'
client_secret = 'your_client_secret_here'
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
        
        c.execute("INSERT INTO spotify_top_100 (title, artist, genre, listeners) VALUES (?, ?, ?, ?)", 
                  (title, artist, genre, listeners))
        
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





# def get_top_tracks(conn):
#     # Connect to database
#     conn = sqlite3.connect('spotify.db')

#     # Initialize Spotify API client with user authorization
#     auth_manager = SpotifyOAuth(
#         client_id="26030839b43a4f679198b03e28a7ba1a",
#         client_secret="e69ba868f41e4029a74096a9d997abae",
#         redirect_uri="http://localhost:8000/callback",
#         scope="user-library-read"
#     )
#     sp = spotipy.Spotify(auth_manager=auth_manager)

#     # Create the tracks table if it doesn't exist
#     c = conn.cursor()
#     c.execute('DROP TABLE IF EXISTS Tracks')
#     c.execute('CREATE TABLE Tracks (id TEXT PRIMARY KEY, name TEXT, genre TEXT, popularity INTEGER)')

#     # Get the first 100 tracks from the playlist
#     results = sp.playlist_tracks('spotify:playlist:3IsxzDS04BvejFJcQ0iVyW', limit=100)

#     # Insert or replace each track in the database
#     for item in results['items']:
#         track = item['track']
#         song_id = track['id']
#         song_genre = sp.artist(track['artists'][0]['uri'])['genres']
#         song_popularity = track['popularity']
#         c.execute('INSERT OR REPLACE INTO Tracks VALUES (?, ?, ?, ?)', (song_id, track['name'], song_genre, song_popularity))

#     # Commit changes and close the database connection
#     conn.commit()
#     conn.close()


# def get_genre_count(conn, genre):
#     """
#     Given a list of songs, returns the number of songs with the given genre in the tracks table.
#     """
#     c = conn.cursor()
#     c.execute("SELECT COUNT(*) FROM Tracks WHERE genre = ?", (genre,))
#     count = c.fetchone()[0]
#     return count


# def get_genre_listeners(conn, genre):
#     """
#     Given a genre, returns the total number of listeners of all songs in that genre.
#     """
#     c = conn.cursor()
#     c.execute("SELECT * FROM Tracks WHERE genre = ?", (genre,))
#     rows = c.fetchall()
#     total_listeners = 0
#     for song in rows:
#         listeners = song[3]  # the popularity is in the 4th column (0-indexed)
#         total_listeners += listeners
#     return total_listeners

# def analyze_data(db_file):
#     # Connect to database
#     conn = sqlite3.connect(db_file)
#     c = conn.cursor()

#     # Query all songs from top 100
#     c.execute("SELECT * FROM Tracks")
#     songs = c.fetchall()

#     # Initialize genre and listener count dictionaries
#     genre_counts = {}
#     listener_counts = {}

#     # Iterate through each song and update genre and listener counts
#     for song in songs:
#         genre = song[2]
#         listeners = song[3]
#         if genre not in genre_counts:
#             genre_counts[genre] = 1
#             listener_counts[genre] = listeners
#         else:
#             genre_counts[genre] += 1
#             listener_counts[genre] += listeners

#     # Print out genre and listener counts
#     print("Spotify Genre Counts:")
#     print(genre_counts)
#     print("Spotify Listener Counts:")
#     print(listener_counts)

#     # Close database connection
#     conn.close()


# def main():
#     # Define database file
#     db_file = "spotify_top100.db"

#     # Check if database file exists
#     if not os.path.exists(db_file):
#         # If not, create a new database file and populate it with top tracks
#         conn = sqlite3.connect(db_file)
#         get_top_tracks(conn)
#     else:
#         # If it exists, analyze the data in the database
#         analyze_data(db_file)


# if __name__ == '__main__':
#     main()