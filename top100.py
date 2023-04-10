import requests
from bs4 import BeautifulSoup
import sqlite3
import os
import matplotlib.pyplot as plt
import pandas as pd

def analyze_data():
    # Set up a connection to the SQLite database
    conn = sqlite3.connect('music_data.db')
    c = conn.cursor()

    # Retrieve the data from the database
    spotify_data = c.execute('SELECT genre, COUNT(*) FROM top_tracks WHERE name LIKE \'%2022%\' GROUP BY genre').fetchall()
    soundcloud_data = c.execute('SELECT genre, COUNT(*) FROM top_tracks GROUP BY genre').fetchall()

    # Calculate the total number of listeners for each platform
    spotify_total_listeners = sum([data[1] for data in spotify_data])
    soundcloud_total_listeners = sum([data[1] for data in soundcloud_data])

    # Calculate the percentage of listeners by genre for each platform
    spotify_genre_percentages = [(data[0], data[1] / spotify_total_listeners * 100) for data in spotify_data]
    soundcloud_genre_percentages = [(data[0], data[1] / soundcloud_total_listeners * 100) for data in soundcloud_data]

    # Create a pie chart of the percentage of listeners by genre for each platform
    plt.subplot(1, 2, 1)
    plt.pie([data[1] for data in spotify_genre_percentages], labels=[data[0] for data in spotify_genre_percentages])
    plt.title('Spotify')

    plt.subplot(1, 2, 2)
    plt.pie([data[1] for data in soundcloud_genre_percentages], labels=[data[0] for data in soundcloud_genre_percentages])
    plt.title('SoundCloud')

    plt.show()

    # Close the connection to the database
    conn.close()