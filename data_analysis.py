import sqlite3


def calculate_genre_percentages(db_file):
    """Calculates the percentage of songs in each genre in the top 100 for each platform"""

    # Connect to the database
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Get the total number of songs for each platform
    spotify_total_songs = c.execute("SELECT COUNT(*) FROM Spotify").fetchone()[0]
    soundcloud_total_songs = c.execute("SELECT COUNT(*) FROM SoundCloud").fetchone()[0]

    # Calculate the number of songs in each genre for each platform
    spotify_genres = c.execute("SELECT genre, COUNT(*) FROM Spotify GROUP BY genre").fetchall()
    soundcloud_genres = c.execute("SELECT genre, COUNT(*) FROM SoundCloud GROUP BY genre").fetchall()

    # Calculate the percentage of songs in each genre for each platform
    spotify_genre_percentages = []
    soundcloud_genre_percentages = []
    for genre, count in spotify_genres:
        percentage = (count / spotify_total_songs) * 100
        spotify_genre_percentages.append((genre, percentage))
    for genre, count in soundcloud_genres:
        percentage = (count / soundcloud_total_songs) * 100
        soundcloud_genre_percentages.append((genre, percentage))

    # Close the database connection
    conn.close()

    return spotify_genre_percentages, soundcloud_genre_percentages


def calculate_listener_percentages(db_file):
    """Calculates the percentage of total listeners for each genre in the top 100 for each platform"""

    # Connect to the database
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Get the total number of listeners for each platform
    spotify_total_listeners = c.execute("SELECT SUM(listeners) FROM Spotify").fetchone()[0]
    soundcloud_total_listeners = c.execute("SELECT SUM(listeners) FROM SoundCloud").fetchone()[0]

    # Calculate the total number of listeners for each genre for each platform
    spotify_genre_listeners = c.execute("SELECT genre, SUM(listeners) FROM Spotify GROUP BY genre").fetchall()
    soundcloud_genre_listeners = c.execute("SELECT genre, SUM(listeners) FROM SoundCloud GROUP BY genre").fetchall()

    # Calculate the percentage of total listeners for each genre for each platform
    spotify_listener_percentages = []
    soundcloud_listener_percentages = []
    for genre, listeners in spotify_genre_listeners:
        percentage = (listeners / spotify_total_listeners) * 100
        spotify_listener_percentages.append((genre, percentage))
    for genre, listeners in soundcloud_genre_listeners:
        percentage = (listeners / soundcloud_total_listeners) * 100
        soundcloud_listener_percentages.append((genre, percentage))

    # Close the database connection
    conn.close()

    return spotify_listener_percentages, soundcloud_listener_percentages

def write_final_report(data):
    with open('final_report.txt', 'w') as f:
        f.write('Data Analysis:\n\n')
        f.write(f'Total number of songs in SoundCloud top 100: {data["soundcloud_total_songs"]}\n')
        f.write(f'Total number of songs in Spotify top 100: {data["spotify_total_songs"]}\n')
        f.write(f'Total number of listeners for SoundCloud: {data["soundcloud_total_listeners"]}\n')
        f.write(f'Total number of listeners for Spotify: {data["spotify_total_listeners"]}\n')
        f.write(f'Average number of listeners per song in SoundCloud top 100: {data["soundcloud_avg_listeners"]}\n')
        f.write(f'Average number of listeners per song in Spotify top 100: {data["spotify_avg_listeners"]}\n\n')
        
        f.write('SoundCloud Visualizations:\n\n')
        f.write(f'SoundCloud Top 100 Genre Distribution:\n{data["soundcloud_genre_distribution"]}\n')
        f.write(f'SoundCloud Top 100 Listener Distribution:\n{data["soundcloud_listener_distribution"]}\n\n')
        
        f.write('Spotify Visualizations:\n\n')
        f.write(f'Spotify Top 100 Genre Distribution:\n{data["spotify_genre_distribution"]}\n')
        f.write(f'Spotify Top 100 Listener Distribution:\n{data["spotify_listener_distribution"]}\n\n')
