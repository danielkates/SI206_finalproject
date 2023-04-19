import requests
import sqlite3
import lyricsgenius
import pandas
from lyricsgenius.api import PublicAPI
import pprint



client_id = "ej2EhnKyOGiOmU4u6c1jWrb3ME57bC_lu1NYruV6nyfx8A7rLCHhMSQZ5x_7UuFQ"
client_secret = "oQUxj0zBXCWht5tkWRoU-543Q5Lvfz4C6pODefEsQF0PWsFdbRsXqd68QA-uJ2lHdUutEDnyTPaXAoqms6q1zg"

def get_top_100_songs():

    genius = lyricsgenius.Genius("7sVvsK_kYL2Ek7UPDDPAwX3-LXDQkiK-hWA8ucfe3yhgP0cGyeJOix6V_bZt6Wy8")
    genius.remove_section_headers = True
    genius.skip_non_songs = True
    genius.excluded_terms = ["(Remix)", "(Live)"]

    conn = sqlite3.connect('all_tables.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS genius
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT,
                  artist TEXT,
                  added_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP);''')
    conn.execute('''CREATE TABLE IF NOT EXISTS genius_artists
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  rank INTEGER,
                  num_popular_songs INTEGER,
                  top_song_rank INTEGER,
                  added_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY(top_song_rank) REFERENCES genius(id));''')

    last_song = conn.execute('''SELECT id FROM genius ORDER BY added_on DESC LIMIT 1''').fetchone()

    if last_song is not None:
        start_page = (last_song[0] // 25) + 1
    else:
        start_page = 1

    count = 0
    for i in range(start_page, start_page + 10):
        api = PublicAPI()
        songs = api.charts(page=i)
        for song in songs['chart_items']:
            title = song['item']['title']
            artist_name = song['item']['primary_artist']['name']
            existing_song = conn.execute("SELECT id FROM genius WHERE title = ? AND artist = ?", (title, artist_name)).fetchone()
            if existing_song is None:
                conn.execute("INSERT INTO genius (title, artist) VALUES (?, ?)", (title, artist_name))
                count += 1
            if count >= 25:
                break
        if count >= 25:
            break

    top_artists = conn.execute('''SELECT artist, COUNT(*) as num_songs
                                   FROM genius GROUP BY artist ORDER BY num_songs DESC LIMIT 10''').fetchall()

    rank_count = 1
    for artist in top_artists:
        name = artist[0]
        rank = rank_count
        num_popular_songs = conn.execute("SELECT COUNT(*) FROM genius WHERE artist = ?", (name,)).fetchone()[0]
        top_song_rank = conn.execute("SELECT MIN(id) FROM genius WHERE artist = ?", (name,)).fetchone()[0]
        conn.execute("INSERT INTO genius_artists (name, rank, num_popular_songs, top_song_rank) VALUES (?, ?, ?, ?)",
                     (name, rank, num_popular_songs, top_song_rank))
        rank_count += 1

    conn.commit()
    conn.close()

    return count
    
def main():
    get_top_100_songs()
if __name__ == '__main__':
    main()