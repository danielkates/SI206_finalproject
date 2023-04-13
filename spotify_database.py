import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3

client_id = 'your_client_id'
client_secret = 'your_client_secret'

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_top_100_songs():
    """
    Returns a list of the top 100 songs from the Spotify API for 2022.
    """
    top_100 = sp.playlist_tracks('playlist_id', offset=0, fields='items.track.name,items.track.artists')
    return top_100


def store_songs_in_database():
    """
    Stores the top 100 songs from the Spotify API for 2022 in a SQLite database.
    """
    conn = sqlite3.connect('spotify_db.sqlite')
    c = conn.cursor()

    # Create table for top 100 songs
    c.execute('''CREATE TABLE IF NOT EXISTS top_100_songs
                (id INTEGER PRIMARY KEY,
                 song_title TEXT,
                 artist TEXT,
                 genre TEXT,
                 num_listeners INTEGER)''')

    top_100 = get_top_100_songs()

    for song in top_100:
        song_title = song['track']['name']
        artist = song['track']['artists'][0]['name']
        genre = ''  # Replace with genre information from an external source, such as Last.fm
        num_listeners = 0  # Replace with number of listeners from an external source, such as Last.fm

        # Insert song into database
        c.execute("INSERT INTO top_100_songs (song_title, artist, genre, num_listeners) VALUES (?, ?, ?, ?)",
                  (song_title, artist, genre, num_listeners))

    conn.commit()
    conn.close()
