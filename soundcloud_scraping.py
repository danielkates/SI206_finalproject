import requests
import sqlite3
import os
import json

# top_url = "https://soundcloud.com/charts/top"
# new_url = "https://soundcloud.com/charts/new"
# track_url "https://soundcloud.com/search/sounds?q="
# artist_url = "https://soundcloud.com/search/people?q="
# genre_url = 
# popularity_url = 

# broswer = webdriver.Chrome()
# browser.get("https://soundcloud.com")

def get_top_100_songs():
    # Scrape top 100 songs from SoundCloud website
    url = 'https://soundcloud.com/charts/top'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    tracks = soup.find_all('li', {'class': 'chartTracks__item'})
    
    # Store data in SQLite database
    conn = sqlite3.connect('music_data.db')
    c = conn.cursor()
    
    for track in tracks:
        title = track.find('h2', {'class': 'trackTitle__title'}).text.strip()
        artist = track.find('a', {'class': 'trackTitle__username'}).text.strip()
        genre = track.find('a', {'class': 'trackTag__title'}).text.strip()
        listeners = track.find('span', {'class': 'sc-visuallyhidden'}).text.strip()
        
        c.execute("INSERT INTO soundcloud_top_100 (title, artist, genre, listeners) VALUES (?, ?, ?, ?)", 
                  (title, artist, genre, listeners))
        
    conn.commit()
    conn.close()

def scrape_soundcloud():
    """
    Scrapes the Soundcloud website and retrieves the top 100 songs from 2022.
    Returns a list of dictionaries where each dictionary contains the following information:
    - Title of the song
    - Artist of the song
    - Genre of the song
    - Total number of listeners of the song
    """
    songs = []
    url = "https://soundcloud.com/charts/top?genre=all-music&date_year=2022&date_month=01-01"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    for item in soup.select(".trackItem"):
        song_dict = {}
        song_dict["title"] = item.select_one(".trackItem__trackTitle").text.strip()
        song_dict["artist"] = item.select_one(".trackItem__username").text.strip()
        song_dict["genre"] = item.select_one(".trackItem__genre").text.strip()
        song_dict["listeners"] = int(item.select_one(".sc-ministats-plays").text.strip().replace(",", ""))
        songs.append(song_dict)

    return songs

def create_soundcloud_table(conn):
    """
    Creates a new table named 'soundcloud' in the database with columns for the title, artist, genre,
    and total number of listeners for each song in the top 100 songs from Soundcloud in 2022.
    """
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS soundcloud
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    artist TEXT NOT NULL,
                    genre TEXT NOT NULL,
                    listeners INTEGER NOT NULL)''')
    conn.commit()

def store_soundcloud_data(conn, songs):
    """
    Stores the data in the 'soundcloud' table in the database.
    """
    cur = conn.cursor()
    for song in songs:
        cur.execute("INSERT INTO soundcloud (title, artist, genre, listeners) VALUES (?, ?, ?, ?)",
                    (song["title"], song["artist"], song["genre"], song["listeners"]))
    conn.commit()

def soundcloud_main():
    """
    The main function for the Soundcloud API/website.
    Scrapes the Soundcloud website, creates a new table in the database, stores the data in the table,
    performs calculations and visualizations, and outputs the results to a file.
    """
    conn = sqlite3.connect('music.db')
    create_soundcloud_table(conn)
    songs = scrape_soundcloud()
    store_soundcloud_data(conn, songs)
    conn.close()
    soundcloud_calculation()
