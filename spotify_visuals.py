import matplotlib.pyplot as plt
import sqlite3

def create_genre_pie_chart():
    # Connect to the database
    conn = sqlite3.connect('music_data.db')
    c = conn.cursor()

    # Get the total number of listeners per genre
    c.execute("SELECT genre, SUM(listeners) FROM spotify GROUP BY genre")
    genre_data = c.fetchall()

    # Create the pie chart
    labels = [row[0] for row in genre_data]
    values = [row[1] for row in genre_data]
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.title('Spotify Top 100 Songs by Genre')
    plt.show()

def create_listener_pie_chart():
    # Connect to the database
    conn = sqlite3.connect('music_data.db')
    c = conn.cursor()

    # Get the total number of listeners per song
    c.execute("SELECT title, listeners FROM spotify ORDER BY listeners DESC")
    listener_data = c.fetchmany(10)

    # Create the pie chart
    labels = [row[0] for row in listener_data]
    values = [row[1] for row in listener_data]
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.title('Spotify Top 10 Most Listened to Songs')
    plt.show()
