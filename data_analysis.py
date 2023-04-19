import sqlite3
import matplotlib.pyplot as plt
import numpy as np

def get_artist_song_count():

    conn = sqlite3.connect('all_tables.db')

    cur = conn.cursor()

    query = """
        SELECT spotify.artist, COUNT(*) AS song_count
        FROM spotify
        JOIN genius ON spotify.artist = genius.artist
        GROUP BY spotify.artist
        ORDER BY song_count DESC;
    """
    cur.execute(query)
    
    results = cur.fetchall()
    

    with open("artist_song_count.txt", "w") as f:
        for (artist, count) in results:
            f.write(f"{artist}: {count}\n")
    
    cur.close()
    conn.close()

def create_artist_count_plot():

    with open("artist_song_count.txt", "r") as f:
        lines = f.readlines()

    artist_names = []
    song_counts = []
    for line in lines:
        artist, count = line.strip().split(": ")
        artist_names.append(artist)
        song_counts.append(int(count))
    
    fig, ax = plt.subplots()
    y_pos = np.arange(len(artist_names))
    ax.barh(y_pos, song_counts)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(artist_names)
    ax.invert_yaxis()
    ax.set_xlabel('Song Count')
    ax.set_ylabel('Artists')
    ax.set_title('Number of Songs by Artist in Top 100')
    plt.show()

def get_common_song_count():
    conn = sqlite3.connect('all_tables.db')
    
    cur = conn.cursor()

    query = """
        SELECT COUNT(*) FROM (
            SELECT DISTINCT spotify.track_name FROM spotify
            JOIN genius ON spotify.track_name = genius.title
        ) AS common_songs;
    """
    cur.execute(query)
    common_song_count = cur.fetchone()[0]
    
    with open("common_song_count.txt", "w") as f:
        f.write(f"{common_song_count} songs are in both top 100 tables.")
    
    cur.close()
    conn.close()

def create_common_song_count_plot():

    with open("common_song_count.txt", "r") as f:
        common_song_count = int(f.readline().strip().split()[0])
    

    fig, ax = plt.subplots()
    ax.bar(['Repeated Songs', 'Unique Songs'], [common_song_count, 195 - common_song_count])
    ax.set_ylabel('Song Count')
    ax.set_title('Number of Songs in Both Top 100 Tables')
    plt.show()

def main():
    get_artist_song_count()
    get_common_song_count()
    create_artist_count_plot()
    create_common_song_count_plot()

if __name__ == '__main__':
    main()