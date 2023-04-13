import sqlite3
import requests
from bs4 import BeautifulSoup

# function to get data from Soundcloud API
def get_soundcloud_data():
    # Soundcloud website URL to scrape
    url = 'https://soundcloud.com/charts/top?genre=all-music&country=US'

    # Send HTTP GET request to Soundcloud website URL and get response
    response = requests.get(url)

    # Create BeautifulSoup object from the HTML content of the response
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all div elements with class "chartTrack"
    chart_tracks = soup.find_all('div', class_='chartTrack')

    # Create empty list to store data
    data = []

    # Loop through chart tracks and extract data for each track
    for track in chart_tracks:
        title = track.find('a', class_='trackTitle').text.strip()
        artist = track.find('a', class_='trackUser').text.strip()
        genre = track.find('span', class_='genreAndBadge').text.strip()
        listeners = int(track.find('span', class_='sc-visuallyhidden').text.strip().replace(',', ''))
        data.append({'title': title, 'artist': artist, 'genre': genre, 'listeners': listeners})

    return data

# function to create table in SQLite database
def create_soundcloud_table():
    # Connect to SQLite database
    conn = sqlite3.connect('music.db')

    # Create cursor object
    c = conn.cursor()

    # Execute SQL to create Soundcloud table
    c.execute('''CREATE TABLE IF NOT EXISTS soundcloud
                (id INTEGER PRIMARY KEY,
                 title TEXT,
                 artist TEXT,
                 genre TEXT,
                 listeners INTEGER)''')

    # Commit changes and close connection
    conn.commit()
    conn.close()

# function to store data in SQLite database
def store_soundcloud_data(data):
    # Connect to SQLite database
    conn = sqlite3.connect('music.db')

    # Create cursor object
    c = conn.cursor()

    # Loop through data and insert into Soundcloud table
    for track in data:
        c.execute("INSERT INTO soundcloud (title, artist, genre, listeners) VALUES (?, ?, ?, ?)",
                  (track['title'], track['artist'], track['genre'], track['listeners']))

    # Commit changes and close connection
    conn.commit()
    conn.close()

# main function to run program
def main():
    soundcloud_data = get_soundcloud_data()
    create_soundcloud_table()
    store_soundcloud_data(soundcloud_data)

if __name__ == "__main__":
    main()
