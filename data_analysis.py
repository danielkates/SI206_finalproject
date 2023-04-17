import sqlite3

def get_artist_song_count():
    # Connect to the database
    conn = sqlite3.connect('all_tables.db')

    # Create a cursor object
    cur = conn.cursor()
    
    # Execute the query to get the artist and song count
    query = """
        SELECT spotify.artist, COUNT(*) AS song_count
        FROM spotify
        JOIN genius ON spotify.artist = genius.artist
        GROUP BY spotify.artist
        ORDER BY song_count DESC;
    """
    cur.execute(query)
    
    # Fetch the results
    results = cur.fetchall()
    
    # Write the results to a text file
    with open("artist_song_count.txt", "w") as f:
        for (artist, count) in results:
            f.write(f"{artist}: {count}\n")
    
    # Clean up
    cur.close()
    conn.close()


def get_common_song_count():
    conn = sqlite3.connect('all_tables.db')
    
    # Create a cursor object
    cur = conn.cursor()
    
    # Execute the query to get the common song count
    query = """
        SELECT COUNT(*) FROM (
            SELECT DISTINCT spotify.track_name FROM spotify
            JOIN genius ON spotify.track_name = genius.title
        ) AS common_songs;
    """
    cur.execute(query)
    common_song_count = cur.fetchone()[0]
    
    # Write the result to a text file
    with open("common_song_count.txt", "w") as f:
        f.write(f"{common_song_count} songs are in both top 100 tables.")
    
    # Clean up
    cur.close()
    conn.close()



def main():
    get_artist_song_count()
    get_common_song_count()

if __name__ == '__main__':
    main()