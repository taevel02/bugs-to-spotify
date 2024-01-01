import sys
import os
import webbrowser

from flask import Flask, redirect
from threading import Timer

from parse import get_bugs_playlist
from dotenv import load_dotenv

from spotify import (
    add_songs_to_playlist,
    create_playlist,
    get_spotify_token,
    search_song,
)

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

app = Flask(__name__)

global access_token

origin_playlist_url = (
    sys.argv[1] if len(sys.argv) > 1 else input("Enter playlist URL: ")
)


@app.route("/auth")
def auth():
    global access_token
    access_token = get_spotify_token()
    return redirect("/")


@app.route("/")
def home():
    return """
    <body>
        <h1>Spotify Playlist Generator</h1>

        <p>1. Click <a href="/auth">here</a> to authenticate.</p>
        <p>2. Click <a href="/generate">here</a> to generate a playlist.</p>
    </body>
    """


@app.route("/generate")
def generate():
    # TODO: Get playlist name from user
    playlist_name = "test"

    playlist_id = create_playlist(playlist_name)

    songs = get_bugs_playlist(origin_playlist_url)

    tracks = []
    for title, artist, album in songs:
        uri = search_song(title, artist, album)
        if uri:
            tracks.append(uri)

    add_songs_to_playlist(playlist_id, tracks)

    return redirect(f"https://open.spotify.com/playlist/{playlist_id}")


def open_browser():
    webbrowser.open_new("http://localhost:8888/")


if __name__ == "__main__":
    Timer(1, open_browser).start()

    app.run(port=8888)
