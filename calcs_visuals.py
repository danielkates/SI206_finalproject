import sqlite3
import os
import seaborn as sns
import matplotlib.pyplot as plt
import csv
import pandas as pd

def create_genre_comparison_chart(genre_counts_spotify, genre_counts_soundcloud):
    """
    Creates a bar chart comparing the number of songs in each genre across Spotify and Soundcloud
    """
    genres = list(genre_counts_spotify.keys())
    spotify_counts = list(genre_counts_spotify.values())
    soundcloud_counts = list(genre_counts_soundcloud.values())

    fig, ax = plt.subplots()
    index = range(len(genres))
    bar_width = 0.35
    opacity = 0.8

    rects1 = ax.bar(index, spotify_counts, bar_width, alpha=opacity, color='b', label='Spotify')
    rects2 = ax.bar(index + bar_width, soundcloud_counts, bar_width, alpha=opacity, color='g', label='Soundcloud')

    ax.set_xlabel('Genre')
    ax.set_ylabel('Number of Songs')
    ax.set_title('Number of Songs per Genre (Spotify vs Soundcloud)')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(genres, rotation=45)
    ax.legend()

    fig.tight_layout()
    plt.show()

def create_listeners_comparison_chart(total_listeners_spotify, total_listeners_soundcloud):
    """
    Creates a bar chart comparing the total number of listeners for each platform
    """
    platforms = ['Spotify', 'Soundcloud']
    listeners = [total_listeners_spotify, total_listeners_soundcloud]

    fig, ax = plt.subplots()
    ax.bar(platforms, listeners)

    ax.set_xlabel('Platform')
    ax.set_ylabel('Total Listeners')
    ax.set_title('Total Listeners per Platform')

    fig.tight_layout()
    plt.show()