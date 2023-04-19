import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3
import pandas as pd

client_id = '26030839b43a4f679198b03e28a7ba1a'
client_secret = 'e69ba868f41e4029a74096a9d997abae'

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def add_next_25_songs():
    """
    Adds the next 25 songs from the Spotify playlist to the 'spotify' table in the 'all_tables.db' database.
    """
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='your_client_id', client_secret='your_client_secret'))

    conn = sqlite3.connect('all_tables.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS spotify
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   track_name TEXT,
                   artist TEXT,
                   popularity INTEGER);''')
    # Get the last added song from the database
    last_song = conn.execute('''SELECT id FROM spotify ORDER BY id DESC LIMIT 1''').fetchone()

    # Set the starting count for the API request
    if last_song is not None:
        count = last_song[0] 
    else:
        count = 0

    # Add the next 25 songs to the 'spotify' table

    results = sp.playlist_tracks('spotify:playlist:3IsxzDS04BvejFJcQ0iVyW', limit=25, offset=count)
    spotify = pd.DataFrame(columns=['Track Name', 'Artist', 'Popularity'])
    for i, item in enumerate(results['items']):
        track = item['track']
        spotify.loc[i] = [track['name'], track['artists'][0]['name'], track['popularity']]
    for i, row in spotify.iterrows():
        track_name = row['Track Name']
        artist = row['Artist']
        popularity = row['Popularity']
        conn.execute("INSERT INTO spotify (track_name, artist, popularity) VALUES (?, ?, ?)", (track_name, artist, popularity))
        count += 1
        if count % 25 == 0:
            break


    # Commit the changes and close the connection
    conn.commit()
    conn.close()



def main():
    add_next_25_songs()
if __name__ == '__main__':
    main()