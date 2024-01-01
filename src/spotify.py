import os
import spotipy

from spotipy.oauth2 import SpotifyOAuth
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = "http://localhost:8888/callback"
scopes = (
    "user-read-private user-read-email playlist-modify-public playlist-modify-private"
)

sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=redirect_uri,
    scope=scopes,
)


def get_spotify_token():
    token_info = sp_oauth.get_cached_token()

    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        print(auth_url)
        response = input(
            "Paste the above link into your browser, then paste the redirect url here: "
        )

        code = sp_oauth.parse_response_code(response)
        token_info = sp_oauth.get_access_token(code) or {}

    return token_info.get("access_token")


def create_playlist(name):
    sp = spotipy.Spotify(auth=get_spotify_token())
    user_id = sp.me()["id"]
    playlist = sp.user_playlist_create(user_id, name)
    return playlist["id"]


def search_song(title, artist, album):
    sp = spotipy.Spotify(auth=get_spotify_token())
    q = quote(f"remaster track:{title} artist:{artist} album:{album}")

    response = sp.search(q=q, type="track")

    if not response["tracks"]["total"]:
        return None

    return response["tracks"]["items"][0]["uri"]


def add_songs_to_playlist(playlist_id, songs):
    sp = spotipy.Spotify(auth=get_spotify_token())
    sp.playlist_add_items(playlist_id, songs)
