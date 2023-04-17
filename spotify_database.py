import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3
import pandas as pd

client_id = '26030839b43a4f679198b03e28a7ba1a'
client_secret = 'e69ba868f41e4029a74096a9d997abae'

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_top_100_songs():
    """
    Returns a list of the top 100 songs from the Spotify API for 2022.
    """
    conn = sqlite3.connect('all_tables.db')
    # Drop the table if it exists
    conn.execute('''DROP TABLE IF EXISTS spotify''')
    # Create the table with popularity column
    conn.execute('''CREATE TABLE spotify
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  track_name TEXT,
                  artist TEXT,
                  popularity INTEGER);''')
    
    count = 0
    for i in range(4):
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
        count += 25
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
    return spotify



def main():
    get_top_100_songs()

if __name__ == '__main__':
    main()