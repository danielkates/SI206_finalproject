import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3

client_id = '26030839b43a4f679198b03e28a7ba1a'
client_secret = 'e69ba868f41e4029a74096a9d997abae'

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_top_100_songs():
    """
    Returns a list of the top 100 songs from the Spotify API for 2022.
    """
    # top_100 = sp.playlist_tracks('playlist_id', offset=0, fields='items.track.name,items.track.artists')
    # return top_100
    results = sp.playlist_tracks('spotify:playlist:3IsxzDS04BvejFJcQ0iVyW', limit=100)
    for i, item in enumerate(results['items']):
        track = item['track']
        print(f"{i+1}: {track['name']} by {track['artists'][0]['name']}")


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

def main():
    # Define database file
    db_file = "Spotify.db"

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