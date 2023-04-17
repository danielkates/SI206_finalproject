import requests
import sqlite3
import lyricsgenius
import pandas
from lyricsgenius.api import PublicAPI
import pprint



client_id = "ej2EhnKyOGiOmU4u6c1jWrb3ME57bC_lu1NYruV6nyfx8A7rLCHhMSQZ5x_7UuFQ"
client_secret = "oQUxj0zBXCWht5tkWRoU-543Q5Lvfz4C6pODefEsQF0PWsFdbRsXqd68QA-uJ2lHdUutEDnyTPaXAoqms6q1zg"



def get_top_100_songs():
    """
    Returns a list of the top 100 songs from the Genius API.
    """
    genius = lyricsgenius.Genius("7sVvsK_kYL2Ek7UPDDPAwX3-LXDQkiK-hWA8ucfe3yhgP0cGyeJOix6V_bZt6Wy8")
    genius.remove_section_headers = True
    genius.skip_non_songs = True
    genius.excluded_terms = ["(Remix)", "(Live)"]

    
    # Create the tables if they don't exist
    conn = sqlite3.connect('all_tables.db')

    conn.execute("DROP TABLE IF EXISTS songs")
    conn.execute("DROP TABLE IF EXISTS artists")
    conn.execute('''CREATE TABLE IF NOT EXISTS genius
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT,
                  artist TEXT);''')
    conn.execute('''CREATE TABLE IF NOT EXISTS genius_artists
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  rank INTEGER,
                  num_popular_songs INTEGER);''')
    
    count = 1
    for i in range(10):
        api = PublicAPI()
        songs = api.charts(page=count) 
        # pprint.pprint(songs)
        # Insert the songs into the 'songs' table
        for song in songs['chart_items']:
            title = song['item']['title']
            artist_name = song['item']['primary_artist']['name']
            # popularity = song['stats']['pageviews']
            conn.execute("INSERT INTO genius (title, artist) VALUES (?, ?)", (title, artist_name))
        count +=1
    
    # Get the top 10 artists based on the number of songs in the 'songs' table
    top_artists = conn.execute('''SELECT artist, COUNT(*) as num_songs
                                   FROM genius GROUP BY artist ORDER BY num_songs DESC LIMIT 10''').fetchall()
    
    # Insert the artists into the 'artists' table
    rank_count = 1
    for artist in top_artists:
        name = artist[0]
        rank = rank_count
        num_popular_songs = conn.execute("SELECT COUNT(*) FROM genius WHERE artist = ?", (name,)).fetchone()[0]
        conn.execute("INSERT INTO genius_artists (name, rank, num_popular_songs) VALUES (?, ?, ?)", (name, rank, num_popular_songs))
        rank_count += 1
    
    # Link the 'songs' and 'artists' tables using a foreign key
    conn.execute('''ALTER TABLE genius ADD COLUMN artist_id INTEGER''')
    conn.execute('''UPDATE genius SET artist_id = (SELECT id FROM genius_artists WHERE genius_artists.name = genius.artist)''')
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
    return songs

    
def main():
    get_top_100_songs()
if __name__ == '__main__':
    main()