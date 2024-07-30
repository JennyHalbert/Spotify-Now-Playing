import tkinter as tk
from tkinter import font 
from tkinter import ttk  
from ttkbootstrap import Style
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import webbrowser
import os
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Environment variables for Spotify API credentials
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID', 'c069f87a76c240ae81e293ef35b9b094')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET', 'fcc4f2fa247148248713ffb090cd1a28')
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'
SCOPE = 'user-read-playback-state user-read-currently-playing'

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SCOPE
))

def get_current_track():
    """Fetches the currently playing track from Spotify."""
    try:
        current_track = sp.current_playback()
        if current_track and current_track['is_playing']:
            track = current_track['item']
            track_name = track['name']
            artist_name = track['artists'][0]['name']
            album_cover_url = track['album']['images'][0]['url'] 
            progress_ms = current_track['progress_ms']
            duration_ms = track['duration_ms']
            return track_name, artist_name, album_cover_url, progress_ms, duration_ms
        else:
            # return "No track is currently playing.", "", None, 0, 0
             return " ", "", None, 0, 0
    except spotipy.exceptions.SpotifyException as e:
        return f"Spotify API error: {e}", "", None, 0, 0

def update_label():
    """Updates the label with the current track information and album cover."""
    track_name, artist_name, album_cover_url, progress_ms, duration_ms = get_current_track()
    track_label.config(text=track_name)
    #artist_label.config(text=f"by {artist_name}")
    artist_label.config(text=f"{artist_name}")

    
    if album_cover_url:
        response = requests.get(album_cover_url)
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        img = img.resize((150, 150))  # Image resize 
        img = ImageTk.PhotoImage(img)
        cover_label.config(image=img)
        cover_label.image = img  # Keep a reference to avoid garbage collection
    else:
        cover_label.config(image='')  # Clear the image if no track is playing

    # Progress bar
    progress_bar['maximum'] = duration_ms
    progress_bar['value'] = progress_ms

    root.after(1000, update_label)  # Update every 0.1 second

def open_spotify_web():
    """Open Spotify Web Player (default browser)."""
    webbrowser.open("https://open.spotify.com")

# Set up the GUI
root = tk.Tk()
root.title("Spotify Now Playing")

style = Style(theme='solar')

# Font styles
track_font = font.Font(family="Times New Roman", size=14, weight="bold")
artist_font = font.Font(family="Times New Roman", size=12)

# Frame for the track info
info_frame = tk.Frame(root)
info_frame.pack(padx=1, pady=10)

# Labels for track name and artist name
track_label = tk.Label(info_frame, text="Fetching current track...", font=track_font)
track_label.pack()
artist_label = tk.Label(info_frame, text="", font=artist_font)
artist_label.pack()

# Display the album cover
cover_label = tk.Label(root)
cover_label.pack(pady=6)

# Progress bar for the song
style = Style(theme='solar')
progress_bar = ttk.Progressbar(root, orient='horizontal', length=155, mode='determinate')
progress_bar.pack(pady=15)

# Create a button to open Spotify Web Player
# open_spotify_button = tk.Button(root, text="Open Spotify", command=open_spotify_web, padx=10, pady=5)
# open_spotify_button.pack(pady=10)


update_label()
root.mainloop()


